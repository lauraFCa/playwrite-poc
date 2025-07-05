using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;

namespace TestingStuff.TestProject.Components;

public class BaseComponent
{
    [ThreadStatic]
    private static IWebDriver? driver;

    public static IWebDriver GetDriver()
    {
        driver ??= new ChromeDriver();

        return driver;
    } 
    
    public static void KillDriver()
    {
        if (driver != null)
        {
            driver.Quit();
            driver.Dispose();
            driver = null;
        }
    }
}
