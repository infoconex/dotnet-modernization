// Separate disposable consumer: actual PackageReference compile and CLR call path.
namespace D2b.Consumer
{
    public static class CallPath
    {
        public static int Run()
        {
            return D2a.Fixture.Probe.Identity();
        }
    }
}
