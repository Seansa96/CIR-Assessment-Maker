using System;
using System.IO;
using System.Reflection;

class Program {
    static void Main() {
        var dll = Assembly.LoadFrom("backend/src/QuizApp.Infrastructure/bin/Debug/net8.0/QuizApp.Infrastructure.dll");
        var repoType = dll.GetType("QuizApp.Infrastructure.Files.FileAssessmentRepository");
        Console.WriteLine(repoType);
    }
}
