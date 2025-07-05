namespace TestingStuff.TestProject.Components;

public class Navigation() : BaseComponent
{
    public void NavigateTo(string url) => GetDriver().Navigate().GoToUrl(url);

}
