#include <Windows.h>
#include <dia2.h>
#include <objbase.h>
#include <oleauto.h>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

#pragma comment(lib, "diaguids.lib")
#pragma comment(lib, "ole32.lib")
#pragma comment(lib, "oleaut32.lib")

using DllGetClassObjectFn = HRESULT(STDAPICALLTYPE*)(REFCLSID, REFIID, void**);

int wmain(int argc, wchar_t** argv)
{
    if (argc != 3) {
        std::wcerr << L"Usage: dia_source_files.exe <signed-msdia140.dll> <locally-built-pdb>\n";
        return 2;
    }
    HRESULT hr = CoInitializeEx(nullptr, COINIT_MULTITHREADED);
    if (FAILED(hr)) return 3;

    HMODULE module = LoadLibraryExW(argv[1], nullptr,
        LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR | LOAD_LIBRARY_SEARCH_DEFAULT_DIRS);
    if (!module) {
        std::wcerr << L"DIA library unavailable\n";
        CoUninitialize();
        return 4;
    }
    auto factoryMethod = reinterpret_cast<DllGetClassObjectFn>(
        GetProcAddress(module, "DllGetClassObject"));
    IClassFactory* factory = nullptr;
    IDiaDataSource* source = nullptr;
    IDiaSession* session = nullptr;
    IDiaEnumTables* tables = nullptr;
    if (!factoryMethod ||
        FAILED(factoryMethod(__uuidof(DiaSource), IID_IClassFactory,
            reinterpret_cast<void**>(&factory))) ||
        FAILED(factory->CreateInstance(nullptr, __uuidof(IDiaDataSource),
            reinterpret_cast<void**>(&source))) ||
        FAILED(source->loadDataFromPdb(argv[2])) ||
        FAILED(source->openSession(&session)) ||
        FAILED(session->getEnumTables(&tables))) {
        std::wcerr << L"DIA failed to open or enumerate PDB (not proof of missing documents)\n";
        return 5;
    }

    unsigned int count = 0;
    unsigned int sourceTables = 0;
    IDiaTable* table = nullptr;
    ULONG fetched = 0;
    while (tables->Next(1, &table, &fetched) == S_OK && fetched == 1) {
        IDiaEnumSourceFiles* files = nullptr;
        if (SUCCEEDED(table->QueryInterface(__uuidof(IDiaEnumSourceFiles),
                reinterpret_cast<void**>(&files)))) {
            ++sourceTables;
            IDiaSourceFile* file = nullptr;
            ULONG fileFetched = 0;
            while (files->Next(1, &file, &fileFetched) == S_OK && fileFetched == 1) {
                BSTR sourceName = nullptr;
                DWORD algorithm = 0;
                DWORD length = 0;
                if (SUCCEEDED(file->get_fileName(&sourceName)) && sourceName != nullptr) {
                    std::wstring name(sourceName, SysStringLen(sourceName));
                    auto position = name.find_last_of(L"\\/");
                    if (position != std::wstring::npos) name = name.substr(position + 1);
                    // Never write absolute paths or raw source contents to CI artifacts.
                    if (FAILED(file->get_checksumType(&algorithm))) algorithm = 0;
                    if (FAILED(file->get_checksum(0, &length, nullptr))) length = 0;
                    std::vector<BYTE> checksum(length);
                    if (length && FAILED(file->get_checksum(length, &length, checksum.data()))) {
                        checksum.clear();
                        length = 0;
                    }
                    std::wcout << L"DOC|" << name << L"|" << algorithm << L"|";
                    for (DWORD i = 0; i < length; ++i) {
                        std::wcout << std::hex << std::setfill(L'0') << std::setw(2)
                            << static_cast<unsigned int>(checksum[i]);
                    }
                    std::wcout << std::dec << L"\n";
                    SysFreeString(sourceName);
                    ++count;
                }
                file->Release();
            }
            files->Release();
        }
        table->Release();
    }
    std::wcout << L"COUNT|" << count << L"|" << sourceTables << L"\n";
    tables->Release();
    session->Release();
    source->Release();
    factory->Release();
    FreeLibrary(module);
    CoUninitialize();
    return 0;
}
