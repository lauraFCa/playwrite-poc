using TestingStuff.TestProject.Data;
using TestingStuff.TestProject.Pages;

namespace TestingStuff.TestProject.Tests;

[TestClass]
public class HomePage : TestBase
{
    [TestMethod]
    public void Test_Form_Page()
    {
        var person = new PersonData()
        {
            FirstName = "John",
            MiddleName = "Doe",
            LastName = "Smith",
            UserId = "johndoe",
            Password = "password",
            AddressLine1 = "1234 Main St"
        };

        new FormPage()
            .FillPersonDataFields<FormPage>(person)
            .RestFormFields<FormPage>();
    }

    [TestMethod]
    [Ignore("Reason to ignore this test")]
    public void Another_Form_Test()
    {
        var person = new PersonData()
        {
            FirstName = "other data",
            LastName = "Smith",
            UserId = "johndoe",
            AddressLine1 = "1234 Main St"
        };

        new FormPage()
            .FillPersonDataFields<FormPage>(person)
            .RestFormFields<FormPage>();
    }

    [TestMethod]
    public void This_Test_Shall_Fail()
    {
        new FormPage()
            .ToFail();
    }
}
