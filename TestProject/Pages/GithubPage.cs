using OpenQA.Selenium;
using TestingStuff.TestProject.Components;

namespace TestingStuff.TestProject.Pages
{
    public class GithubPage
    {
        public GithubPage GoToGithub()
        {
            new Navigation().NavigateTo("https://github.com");
            return this;
        }

        public GithubPage ValidateHomePage()
        {
            new Label(By.CssSelector("section h1"))
                .ValidateValue("Build and ship software on a single, collaborative platform", "textContent");
            return this;
        }
    }
}
