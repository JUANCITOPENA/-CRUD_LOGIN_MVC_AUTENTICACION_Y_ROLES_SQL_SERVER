using Microsoft.Maui.Controls;
using Microsoft.Data.SqlClient;
using System.Data;

using CRUD_LOGIN_MAUI.Controllers;

namespace CRUD_LOGIN_MAUI.Views;

public partial class MainPage : ContentPage
{
    public MainPage()
    {
        InitializeComponent();
    }

    protected override void OnAppearing()
    {
        base.OnAppearing();
        txtUsuario.Text = string.Empty;
        txtPassword.Text = string.Empty;
        lblMensaje.Text = string.Empty;
    }

    private void OnTogglePasswordClicked(object sender, EventArgs e)
    {
        txtPassword.IsPassword = !txtPassword.IsPassword;
        btnTogglePassword.Text = txtPassword.IsPassword ? "👁️" : "🙈";
    }

    private async void OnLogin_Clicked(object sender, EventArgs e)
    {
        string usuario = txtUsuario.Text?.Trim();
        string password = txtPassword.Text?.Trim();

        if (string.IsNullOrWhiteSpace(usuario) || string.IsNullOrWhiteSpace(password))
        {
            lblMensaje.Text = "❌ Por favor, ingrese sus credenciales.";
            return;
        }

        try
        {
            string connectionString = Config.ConnectionString;

            using (var connection = new SqlConnection(connectionString))
            {
                await connection.OpenAsync();

                string query = @"SELECT R.NombreRol 
                                 FROM Usuarios U 
                                 INNER JOIN Roles R ON U.IdRol = R.Id 
                                 WHERE U.Usuario = @Usuario 
                                 AND U.Password = CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', @Password), 2)";

                using (var command = new SqlCommand(query, connection))
                {
                    command.Parameters.Add("@Usuario", SqlDbType.VarChar, 50).Value = usuario;
                    command.Parameters.Add("@Password", SqlDbType.VarChar, 50).Value = password;

                    var roleResult = await command.ExecuteScalarAsync();

                    if (roleResult != null)
                    {
                        string role = roleResult.ToString();
                        await Shell.Current.GoToAsync($"{role}Page");
                    }
                    else
                    {
                        lblMensaje.Text = "❌ Usuario o contraseña incorrectos.";
                    }
                }
            }
        }
        catch (Exception ex)
        {
            lblMensaje.Text = $"❌ Error: {ex.Message}";
        }
    }
}


