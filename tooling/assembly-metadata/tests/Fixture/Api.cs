using System;
using System.Collections.Generic;

namespace Fixture.Namespace;

public interface IContract<T>
{
    T Convert(T input);
}

public enum Kind : short { One = 1, Two = 2 }
public delegate string Formatter(int value);
public class Sample<T> : IContract<T> where T : class, new()
{
    public T Value { get; set; } = new();
    public event EventHandler? Changed;
    public const int Number = 42;
    public void WithDefault(int count = 7) { }

    public readonly int ReadOnly;
    internal int Invisible;
    protected internal virtual T Process(ref T value, out string? message) { message = null; return value; }
    public T Convert(T input) => input;
    public static string Echo(string text) => text;
    public static string Echo(int number) => number.ToString();
    public U Adapt<U>(T source, U fallback) where U : struct => fallback;
    public class Nested { public void Ping() { } }
    private class Hidden { public void No() { } }
}
internal class Secret { public void Hidden() { } }
