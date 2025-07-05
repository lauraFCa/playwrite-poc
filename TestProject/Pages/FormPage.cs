using TestingStuff.TestProject.Components;
using TestingStuff.TestProject.Data;
using OpenQA.Selenium;

namespace TestingStuff.TestProject.Pages;

class FormPage
{
    public FormPage() { }

    public T RestFormFields<T>() where T : new()
    {
        new Button(By.CssSelector(".container p input")).ClickWithJS();
        return new T();
    }

    public T FillPersonDataFields<T>(PersonData data) where T : new()
    {
        new Input(By.CssSelector("[name='02frstname']")).TypeIn(data.FirstName);
        new Input(By.CssSelector("[name='03middle_i']")).TypeIn(data.MiddleName);
        new Input(By.CssSelector("[name='04lastname']")).TypeIn(data.LastName);
        new Input(By.CssSelector("[name='30_user_id']")).TypeIn(data.UserId);
        new Input(By.CssSelector("[name='31password']")).TypeIn(data.Password);
        new Input(By.CssSelector("[name='10address1']")).TypeIn(data.AddressLine1);
        return new T();
    }

    public static T SendForm<T>() where T : new()
    {
        new Button(By.CssSelector(".get-button")).Click();
        return new T();
    }

    public void ToFail()
    {
        new Input(By.CssSelector("not exists")).TypeIn("this will fail");
    }

}
