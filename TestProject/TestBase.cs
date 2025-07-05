using TestingStuff.TestProject.Components;
using Microsoft.Extensions.Configuration;
using System.Text.Json.Nodes;

namespace TestingStuff.TestProject;

public class TestBase : BaseComponent
{
    public IConfiguration? Configuration { get; private set; }

    [TestInitialize]
    public void TestInitialize()
    {
        if(Configuration == null)
            ReadConfigs();

        GetDriver().Navigate().GoToUrl(Configuration?["baseUrl"]);
    }

    [TestCleanup]
    public void TestCleanup()
    {
        KillDriver();
    }

    private void ReadConfigs()
    {
        Configuration = new ConfigurationBuilder()
            .AddInMemoryCollection(
                ReadJsonFile(
                    "appsettings.json"
                )
            )
            .Build();
    }

    private static Dictionary<string, string?> ReadJsonFile(string filePath)
    {
        var json = File.ReadAllText(filePath);
        var jsonObject = JsonNode.Parse(json)?.AsObject();
        var configDictionary = new Dictionary<string, string?>();

        if (jsonObject != null)
        {
            foreach (var kvp in jsonObject)
            {
                configDictionary[kvp.Key] = kvp.Value?.ToString();
            }
        }

        return configDictionary;
    }
}
