// Synthetic, public, immutable fixture; same source bytes compile in both variants.
namespace D2a.Fixture
{
    public static class Probe
    {
        public static int Identity()
        {
#if D2A_ALT
            return 202;
#else
            return 101;
#endif
        }
    }
}
