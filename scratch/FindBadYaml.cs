using System;
using System.IO;
using System.Reflection;

class Program
{
    static void Main()
    {
        var repoAssm = Assembly.LoadFrom(@"backend\src\QuizApp.Infrastructure\bin\Debug\net8.0\QuizApp.Infrastructure.dll");
        var coreAssm = Assembly.LoadFrom(@"backend\src\QuizApp.Core\bin\Debug\net8.0\QuizApp.Core.dll");
        
        var formatType = repoAssm.GetType("QuizApp.Infrastructure.Files.FileFormat");
        var readMethod = formatType.GetMethod("ReadAsync");
        var docType = coreAssm.GetType("QuizApp.Core.Models.AssessmentDocument");
        var genericRead = readMethod.MakeGenericMethod(docType);

        var token = new System.Threading.CancellationToken();

        foreach (var file in Directory.GetFiles(@"data\assessments", "*.yaml"))
        {
            try
            {
                var task = (System.Threading.Tasks.Task)genericRead.Invoke(null, new object[] { file, token });
                task.GetAwaiter().GetResult();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"ERROR IN FILE: {file}");
                Console.WriteLine(ex.ToString());
            }
        }
    }
}
