
using TestingStuff.TestProject.Pages;

namespace TestingStuff.TestProject.Tests;

[TestClass]
public class GithubHomeTests : TestBase
{
    [TestMethod]
    public void Validate_Github_HomePage()
    {
        new GithubPage()
            .GoToGithub()
            .ValidateHomePage();
    }
}