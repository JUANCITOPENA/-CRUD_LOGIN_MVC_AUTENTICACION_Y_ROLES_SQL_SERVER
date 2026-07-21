using CRUD_LOGIN_MAUI.Controllers;

namespace CRUD_LOGIN_MAUI.Views;

public partial class VendedorPage : ContentPage
{
    public VendedorPage()
    {
        InitializeComponent();
    }

    private async void OnLogoutClicked(object sender, EventArgs e)
    {
        await Shell.Current.GoToAsync("//MainPage");
    }
}

