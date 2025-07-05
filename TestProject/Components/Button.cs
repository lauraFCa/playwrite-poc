using OpenQA.Selenium;

namespace TestingStuff.TestProject.Components;
public class Button(By locator) : BaseComponent
{
    protected By Locator { get; set; } = locator;

    public void Click()
    {
        GetDriver().FindElement(Locator).Click();
    }

    public void ClickWithJS()
    {
        var button = GetDriver().FindElement(Locator);
        IJavaScriptExecutor executor = (IJavaScriptExecutor)GetDriver();
        executor.ExecuteScript("arguments[0].click();", button);
    }
}
