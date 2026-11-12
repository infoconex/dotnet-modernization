// EXP-042: research-only MSBuild structured TaskInput event recorder.
// Compiled against the installed Visual Studio MSBuild.Framework assembly.
// NO task parameter, path or hash is written to stdout. Private file only.
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Microsoft.Build.Framework;

public sealed class RecordSiftResearchCscParameterLogger : ILogger
{
    private readonly object gate = new object();
    private readonly HashSet<int> cscTaskIds = new HashSet<int>();
    private readonly Dictionary<int, List<string>> inputs = new Dictionary<int, List<string>>();
    public string Parameters { get; set; }
    public LoggerVerbosity Verbosity { get; set; }

    public void Initialize(IEventSource source)
    {
        if (String.IsNullOrWhiteSpace(Parameters))
            throw new LoggerException("EXP042_PRIVATE_LOGGER_OUTPUT_MISSING");
        Verbosity = LoggerVerbosity.Diagnostic;
        source.TaskStarted += delegate(object sender, TaskStartedEventArgs e)
        {
            if (String.Equals(e.TaskName, "Csc", StringComparison.OrdinalIgnoreCase) &&
                e.BuildEventContext != null)
            {
                lock (gate) { cscTaskIds.Add(e.BuildEventContext.TaskId); }
            }
        };
        source.MessageRaised += delegate(object sender, BuildMessageEventArgs e)
        {
            var task = e as TaskParameterEventArgs;
            if (task == null || task.Kind != TaskParameterMessageKind.TaskInput ||
                !String.Equals(task.ParameterName, "Sources", StringComparison.OrdinalIgnoreCase) ||
                task.BuildEventContext == null || task.Items == null)
                return;
            var values = new List<string>();
            foreach (object item in task.Items)
            {
                var buildItem = item as ITaskItem;
                string spec = buildItem != null ? buildItem.ItemSpec :
                    (item == null ? null : item.ToString());
                if (String.IsNullOrWhiteSpace(spec) || spec.Length > 8192)
                    throw new LoggerException("EXP042_INVALID_CSC_STRUCTURED_SOURCE_ITEM");
                values.Add(spec);
            }
            lock (gate)
            {
                int id = task.BuildEventContext.TaskId;
                if (inputs.ContainsKey(id))
                    throw new LoggerException("EXP042_DUPLICATE_CSC_TASK_PARAMETER_EVENT");
                inputs.Add(id, values);
            }
        };
    }

    public void Shutdown()
    {
        try
        {
            List<List<string>> chosen;
            lock (gate)
            {
                chosen = inputs.Where(x => cscTaskIds.Contains(x.Key))
                               .Select(x => x.Value).ToList();
            }
            if (chosen.Count != 1 || chosen[0].Count < 1 || chosen[0].Count > 1024)
            {
                File.WriteAllText(Parameters, "STATUS\tNO_UNIQUE_CSC_SOURCE_EVENT\n",
                                  Encoding.ASCII);
                return;
            }
            using (var writer = new StreamWriter(Parameters, false, Encoding.ASCII))
            {
                writer.WriteLine("STATUS\tCSC_TASK_PARAMETER_EVENT");
                writer.WriteLine("COUNT\t" + chosen[0].Count);
                foreach (string spec in chosen[0])
                    writer.WriteLine(Convert.ToBase64String(Encoding.UTF8.GetBytes(spec)));
            }
        }
        catch (Exception)
        {
            // No exception payload, source names, diagnostics or paths ever logged.
            throw new LoggerException("EXP042_PRIVATE_STRUCTURED_LOGGER_FAILED");
        }
    }
}
