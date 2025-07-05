using OpenQA.Selenium;

namespace TestingStuff.TestProject.Components;

public class Input(By locator) : BaseComponent
{
    protected By Locator { get; set; } = locator;

    public void TypeIn(string? text)
    {
        if (!string.IsNullOrEmpty(text))
        {
            GetDriver().FindElement(Locator).SendKeys(text);
        }
    }
}
