using System;
using System.IO;
using System.Reflection;

class Program
{
    static void Main()
    {
        var basePath = @"C:\Users\SeanS\Downloads\cir_app";
        var repoAssm = Assembly.LoadFrom(Path.Combine(basePath, @"backend\src\QuizApp.Infrastructure\bin\Debug\net8.0\QuizApp.Infrastructure.dll"));
        
        var formatType = repoAssm.GetType("QuizApp.Infrastructure.Files.FileFormat");
        var readMethod = formatType.GetMethod("ReadAsync");
        var docType = repoAssm.GetType("QuizApp.Infrastructure.Files.AssessmentFileDto");
        var genericRead = readMethod.MakeGenericMethod(docType);

        var token = new System.Threading.CancellationToken();

        foreach (var file in Directory.GetFiles(Path.Combine(basePath, @"data\assessments"), "*.yaml"))
        {
            try
            {
                var task = (System.Threading.Tasks.Task)genericRead.Invoke(null, new object[] { file, token });
                task.GetAwaiter().GetResult();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n===================\nERROR IN FILE: {Path.GetFileName(file)}\n{ex.InnerException?.Message ?? ex.Message}\n===================\n");
            }
        }
    }
}
