using OpenQA.Selenium;

namespace TestingStuff.TestProject.Components;

public class Label(By locator) : BaseComponent
{
    protected By Locator { get; set; } = locator;

    public void ValidateValue(string expectedValue, string attribute = "value")
    {
        var realValue = GetDriver().FindElement(Locator).GetAttribute(attribute);
        if (!string.Equals(realValue, expectedValue))
            throw new Exception($"The value of the label is incorrect. Expected: {expectedValue}. Real: {realValue}");
    }
}
