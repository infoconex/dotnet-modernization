// D2a: trusted-Windows research-only single-Csc task witness.
// Private task context and source count ONLY. No source paths or commands printed.
// This logger is NOT a cryptographic Csc-to-output attestation provider.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Microsoft.Build.Framework;

public sealed class D2aCscWitnessLogger : ILogger
{
    private readonly object gate = new object();
    private readonly HashSet<string> started = new HashSet<string>(StringComparer.Ordinal);
    private readonly HashSet<string> sources = new HashSet<string>(StringComparer.Ordinal);
    private readonly HashSet<string> finished = new HashSet<string>(StringComparer.Ordinal);
    private readonly Dictionary<string, int> counts = new Dictionary<string, int>(StringComparer.Ordinal);

    public string Parameters { get; set; }
    public LoggerVerbosity Verbosity { get; set; }

    private static string Identity(BuildEventContext context)
    {
        if (context == null)
        {
            return null;
        }

        return context.NodeId + ":" + context.ProjectContextId + ":" +
               context.TargetId + ":" + context.TaskId;
    }

    public void Initialize(IEventSource source)
    {
        if (String.IsNullOrWhiteSpace(Parameters))
        {
            throw new LoggerException("D2A_WITNESS_OUTPUT_MISSING");
        }

        Verbosity = LoggerVerbosity.Diagnostic;

        source.TaskStarted += delegate(object sender, TaskStartedEventArgs e)
        {
            if (String.Equals(e.TaskName, "Csc", StringComparison.OrdinalIgnoreCase))
            {
                string key = Identity(e.BuildEventContext);
                lock (gate)
                {
                    if (key != null)
                    {
                        started.Add(key);
                    }
                }
            }
        };

        source.MessageRaised += delegate(object sender, BuildMessageEventArgs e)
        {
            var input = e as TaskParameterEventArgs;
            if (input == null || input.Kind != TaskParameterMessageKind.TaskInput ||
                !String.Equals(input.ParameterName, "Sources", StringComparison.OrdinalIgnoreCase) ||
                input.Items == null)
            {
                return;
            }

            string key = Identity(input.BuildEventContext);
            lock (gate)
            {
                if (key != null)
                {
                    sources.Add(key);
                    if (counts.ContainsKey(key))
                    {
                        throw new LoggerException("D2A_DUPLICATE_CSC_SOURCE_EVENT");
                    }
                    counts.Add(key, input.Items.Cast<object>().Count());
                }
            }
        };

        source.TaskFinished += delegate(object sender, TaskFinishedEventArgs e)
        {
            if (String.Equals(e.TaskName, "Csc", StringComparison.OrdinalIgnoreCase) &&
                e.Succeeded)
            {
                string key = Identity(e.BuildEventContext);
                lock (gate)
                {
                    if (key != null)
                    {
                        finished.Add(key);
                    }
                }
            }
        };
    }

    public void Shutdown()
    {
        try
        {
            string row;
            lock (gate)
            {
                bool valid = started.Count == 1 && sources.Count == 1 &&
                             finished.Count == 1 &&
                             started.SetEquals(sources) && started.SetEquals(finished);
                string key = valid ? started.Single() : null;
                valid = valid && counts.ContainsKey(key) &&
                        counts[key] >= 1 && counts[key] <= 16;
                row = valid ? "STATUS\tUNIQUE_COMPLETED_CSC\t" + key +
                              "\t" + counts[key] + "\n"
                            : "STATUS\tINVALID_CSC_EVENT_CONTEXT\n";
            }

            File.WriteAllText(Parameters, row, Encoding.ASCII);
        }
        catch (Exception)
        {
            throw new LoggerException("D2A_PRIVATE_CSC_WITNESS_FAILURE");
        }
    }
}
