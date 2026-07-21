# 🔐 CRUD_LOGIN_MAUI — Sistema de Autenticación y Roles (Versión MVC)

> 📘 **Manual paso a paso, completo y documentado**
> Guía exhaustiva para construir un sistema de **login con roles** desarrollado en **.NET MAUI**, con conexión a **SQL Server**, contraseñas protegidas mediante **hashing SHA2_256** y estructurado con el **Patrón MVC**.

---

## 📑 Tabla de Contenidos

| # | Paso | Descripción |
|---|------|-------------|
| 🧠 | [Contexto MVC](#-por-qué-mvc-y-no-el-código-anterior) | Teoría y ventajas de la arquitectura MVC |
| 🗄️ | [Paso 1](#-paso-1-configurar-la-base-de-datos-sql-server) | Configurar la Base de Datos (SQL Server) |
| 🚀 | [Paso 2](#-paso-2-enrutamiento-principal-appshell) | Enrutamiento Principal (AppShell) |
| 🔒 | [Paso 3](#-paso-3-pantalla-de-login-mainpage) | Pantalla de Login (MainPage) |
| 🛠️ | [Paso 4](#-paso-4-panel-de-control-adminpage) | Panel de Control (AdminPage) |
| 🎭 | [Paso 5](#-paso-5-vistas-roles) | Vista de Gestión de Roles |
| 👔 | [Paso 6](#-paso-6-vistas-limitadas-supervisor) | Vista Restringida — Supervisor |
| 🛍️ | [Paso 7](#-paso-7-vistas-limitadas-vendedor) | Vista Restringida — Vendedor |
| ✅ | [Cierre](#-conclusión) | Conclusión y buenas prácticas |

---

## 🧠 ¿Por qué MVC y no el código anterior?

En la versión anterior teníamos una arquitectura monolítica (*Code-Behind* pesado). Las clases de datos, la configuración y el diseño visual vivían amontonados.

Al evolucionar a **MVC (Modelo-Vista-Controlador)** separamos responsabilidades:
- **Models (Modelos):** Aquí viven nuestras clases de datos (ej. UsuarioItem.cs, RolItem.cs). Representan la información pura.
- **Views (Vistas):** Contienen exclusivamente las pantallas (.xaml y .xaml.cs).
- **Controllers (Controladores):** Alojan la configuración (Config.cs) y orquestan la base de datos. 

**¿Por qué es mejor?**
1. **Orden:** Sabes exactamente dónde encontrar cada cosa.
2. **Reutilización:** Las clases de los *Models* pueden ser usadas por varias pantallas.
3. **Escalabilidad Sencilla:** Un proyecto muy profesional sin llegar a la extrema complejidad de MVVM.

---

## 🧭 Visión General del Proyecto

- 🔑 **Login seguro** (SQL Server + SHA2_256).
- 🧩 **Navegación basada en Shell**.
- 🗂️ **CRUD completo** de usuarios y roles.
- 🎨 **Vistas diferenciadas por rol**.

`	ext
📁 CRUD_LOGIN_MAUI
 ├── 📁 Models                  # 🧠 MODELOS (Datos)
 │    ├── 📄 UsuarioItem.cs
 │    └── 📄 RolItem.cs
 │
 ├── 📁 Views                   # 🎨 VISTAS (Pantallas)
 │    ├── 📄 MainPage.xaml / .cs
 │    ├── 📄 AdminPage.xaml / .cs
 │    ├── 📄 RolesPage.xaml / .cs
 │    ├── 📄 SupervisorPage.xaml / .cs
 │    └── 📄 VendedorPage.xaml / .cs
 │
 ├── 📁 Controllers             # ⚙️ CONTROLADORES
 │    └── 📄 Config.cs          
 │
 ├── 📄 App.xaml / .cs          
 ├── 📄 AppShell.xaml / .cs     
 └── 📄 CRUD_LOGIN_MAUI.csproj  
`

---

## 🗄️ PASO 1: Configurar la Base de Datos (SQL Server)

`sql
CREATE DATABASE LoginRolesDB_cif;
GO
USE LoginRolesDB_cif;
GO

CREATE TABLE Roles (
    Id INT PRIMARY KEY IDENTITY(1,1),
    NombreRol VARCHAR(50) NOT NULL
);

CREATE TABLE Usuarios (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Usuario VARCHAR(50) NOT NULL,
    Password VARCHAR(64) NOT NULL,
    IdRol INT FOREIGN KEY REFERENCES Roles(Id)
);

INSERT INTO Roles (NombreRol) VALUES ('Admin'), ('Supervisor'), ('Vendedor');

INSERT INTO Usuarios (Usuario, Password, IdRol) VALUES
('AdminUser', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'admin123'), 2), 1),
('SuperUser', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'super123'), 2), 2),
('SalesUser', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'sales123'), 2), 3);
GO
`

---

## 🚀 PASO 2: Enrutamiento Principal (AppShell)

### 🛠️ Inicialización Base (App.xaml.cs)

``csharp
using Microsoft.Extensions.DependencyInjection;

namespace CRUD_LOGIN_MAUI;

public partial class App : Application
{
    public App()
    {
        InitializeComponent();
    }

    protected override Window CreateWindow(IActivationState? activationState)
    {
        return new Window(new AppShell());
    }
}

``

### 📄 Editar el archivo AppShell.xaml

``xml
<?xml version="1.0" encoding="UTF-8" ?>
<Shell
    x:Class="CRUD_LOGIN_MAUI.AppShell"
    xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
    xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
    xmlns:local="clr-namespace:CRUD_LOGIN_MAUI"
    xmlns:views="clr-namespace:CRUD_LOGIN_MAUI.Views"
    Title="CRUD_LOGIN_MAUI"
    FlyoutBehavior="Disabled">
    <!-- Deshabilita el menú deslizable -->

    <!-- Página de Inicio por Defecto (Login) -->
    <ShellContent
        Title="Home"
        ContentTemplate="{DataTemplate views:MainPage}"
        Route="MainPage" />

    <!-- Rutas ocultas en el menú, solo accesibles por código C# -->
    <ShellContent Route="AdminPage" ContentTemplate="{DataTemplate views:AdminPage}" FlyoutItem.IsVisible="False"/>
    <ShellContent Route="SupervisorPage" ContentTemplate="{DataTemplate views:SupervisorPage}" FlyoutItem.IsVisible="False"/>
    <ShellContent Route="VendedorPage" ContentTemplate="{DataTemplate views:VendedorPage}" FlyoutItem.IsVisible="False"/>
</Shell>

``

### ⚙️ Archivo AppShell.xaml.cs

``csharp
using CRUD_LOGIN_MAUI.Views;

namespace CRUD_LOGIN_MAUI;

public partial class AppShell : Shell
{
    public AppShell()
    {
        InitializeComponent();

        // Registrar rutas para poder navegar a ellas usando Shell.Current.GoToAsync()
        Routing.RegisterRoute("AdminPage", typeof(AdminPage));
        Routing.RegisterRoute("SupervisorPage", typeof(SupervisorPage));
        Routing.RegisterRoute("VendedorPage", typeof(VendedorPage));
        Routing.RegisterRoute("RolesPage", typeof(RolesPage));
    }
}

``

---

## 🔒 PASO 3: Pantalla de Login (MainPage)

### ⚙️ Centralizar la Conexión (Config.cs en Controllers)

``csharp
namespace CRUD_LOGIN_MAUI.Controllers;

public static class Config
{
    public const string ConnectionString = "Server=10.0.0.15,1433;Database=LoginRolesDB_cif;User Id=JUANCITO;Password=123456;TrustServerCertificate=True;";
}

``

### 🎨 Diseño (Views/MainPage.xaml)

``xml
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="CRUD_LOGIN_MAUI.Views.MainPage">

    <VerticalStackLayout Padding="30" Spacing="20" BackgroundColor="#F5F5F5">

        <Image Source="https://images.icon-icons.com/2120/PNG/512/lock_padlock_locked_protected_security_icon_131240.png"
               HeightRequest="175" HorizontalOptions="Center" />

        <Entry x:Name="txtUsuario"
               Placeholder="Usuario"
               ClearButtonVisibility="WhileEditing"
               HorizontalTextAlignment="Center"
               TextColor="Black"
               FontSize="25"
               Margin="10"/>

        <!-- Grid para Contrase�a + Bot�n Ojito -->
        <Grid Margin="10">
            <Entry x:Name="txtPassword"
                   Placeholder="Contrase�a"
                   IsPassword="True"
                   HorizontalTextAlignment="Center"
                   TextColor="Black"
                   FontSize="25"/>

            <Button x:Name="btnTogglePassword"
                    Text="???"
                    Clicked="OnTogglePasswordClicked"
                    BackgroundColor="Transparent"
                    HorizontalOptions="End"
                    WidthRequest="60"/>
        </Grid>

        <Button Text="Ingresar"
                BackgroundColor="#fbc531"
                TextColor="#40739e"
                FontAttributes="Bold"
                Margin="20"
                Clicked="OnLogin_Clicked"
                FontSize="25" />

        <Label x:Name="lblMensaje"
               TextColor="Red"
               FontSize="22"
               FontAttributes="Bold"
               HorizontalTextAlignment="Center" />

    </VerticalStackLayout>
</ContentPage>



``

### 🧠 Lógica de Views/MainPage.xaml.cs

``csharp
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



``

---

## 🛠️ PASO 4: Panel de Control (AdminPage)

### 🧠 El Modelo (Models/UsuarioItem.cs)

``csharp
namespace CRUD_LOGIN_MAUI.Models;

public class UsuarioItem
{
    public int Id { get; set; }
    public string Usuario { get; set; }
    public string Rol { get; set; }
}

``

### 🎨 La Vista (Views/AdminPage.xaml)

``xml
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:local="clr-namespace:CRUD_LOGIN_MAUI.Views"
             xmlns:models="clr-namespace:CRUD_LOGIN_MAUI.Models"
             x:Class="CRUD_LOGIN_MAUI.Views.AdminPage"
             Title="Administrador">

    <ScrollView>
        <VerticalStackLayout Padding="20" Spacing="15" BackgroundColor="#E3F2FD">

            <!-- Título -->
            <Label Text="Panel de Control - Administrador"
                   FontSize="22"
                   FontAttributes="Bold"
                   TextColor="#0D47A1"
                   HorizontalOptions="Center"/>

            <!-- Entradas de usuario -->
            <Entry x:Name="txtUsuario" Placeholder="👤 Usuario"/>
            <Entry x:Name="txtPassword" Placeholder="🔑 Contraseña" IsPassword="True"/>

            <!-- Picker de roles -->
            <Picker x:Name="pickerRol" Title="Seleccionar Rol">
                <Picker.ItemsSource>
                    <x:Array Type="{x:Type x:String}">
                        <x:String>Admin</x:String>
                        <x:String>Supervisor</x:String>
                        <x:String>Vendedor</x:String>
                    </x:Array>
                </Picker.ItemsSource>
            </Picker>

            <!-- Buscador -->
            <Entry x:Name="txtBuscar"
                   Placeholder="🔎 Buscar por ID, Usuario o Rol..."
                   TextChanged="OnSearchChanged"
                   BackgroundColor="White"/>

            <!-- Botones CRUD -->
            <Grid ColumnDefinitions="*,*,*" RowDefinitions="Auto,Auto" ColumnSpacing="10" RowSpacing="10">
                <Button Grid.Row="0" Grid.Column="0" Text="➕ Insertar" BackgroundColor="Green" TextColor="White" Clicked="OnInsertClicked"/>
                <Button Grid.Row="0" Grid.Column="1" Text="🔄 Actualizar" BackgroundColor="DodgerBlue" TextColor="White" Clicked="OnUpdateClicked"/>
                <Button Grid.Row="0" Grid.Column="2" Text="🗑️ Eliminar" BackgroundColor="Red" TextColor="White" Clicked="OnDeleteClicked"/>
                <Button Grid.Row="1" Grid.Column="0" Text="🔍 Consultar" BackgroundColor="Orange" TextColor="White" Clicked="OnConsultClicked"/>
                <Button Grid.Row="1" Grid.Column="1" Text="✅ Validar" BackgroundColor="Purple" TextColor="White" Clicked="OnValidateClicked"/>
                <Button Grid.Row="1" Grid.Column="2" Text="🧹 Limpiar" BackgroundColor="Gray" TextColor="White" Clicked="OnClearClicked"/>
            </Grid>

            <!-- Mensajes -->
            <Label x:Name="lblMensaje" TextColor="Red" FontAttributes="Bold" HorizontalOptions="Center"/>

            <!-- Lista de usuarios con compiled bindings -->
            <CollectionView x:Name="listaUsuarios"
                            SelectionMode="Single"
                            SelectionChanged="OnUsuarioSelected"
                            HeightRequest="250">
                <CollectionView.ItemTemplate>
                    <DataTemplate x:DataType="models:UsuarioItem">
                        <Grid Padding="10" ColumnDefinitions="40, *, *">
                            <Label Grid.Column="0" Text="{Binding Id}" FontAttributes="Bold" TextColor="Blue"/>
                            <Label Grid.Column="1" Text="{Binding Usuario}" FontAttributes="Bold"/>
                            <Label Grid.Column="2" Text="{Binding Rol}" TextColor="Gray"/>
                        </Grid>
                    </DataTemplate>
                </CollectionView.ItemTemplate>
            </CollectionView>

            <Button Text="⚙️ Roles"
                    BackgroundColor="Teal"
                    TextColor="White"
                    Clicked="OnRolesClicked"/>


            <!-- Botón logout -->
            <Button Text="Cerrar sesión"
                    BackgroundColor="DarkRed"
                    TextColor="White"
                    Margin="0,20"
                    Clicked="OnLogoutClicked"/>
        </VerticalStackLayout>
    </ScrollView>
</ContentPage>





``

### 🧩 Lógica (Views/AdminPage.xaml.cs)

``csharp
using Microsoft.Data.SqlClient;
using System.Data;

using CRUD_LOGIN_MAUI.Models;
using CRUD_LOGIN_MAUI.Controllers;

namespace CRUD_LOGIN_MAUI.Views;



public partial class AdminPage : ContentPage
{
    private string connectionString = Config.ConnectionString;
    private bool isProcessing = false;
    private int idSeleccionado = 0;
    private List<int> _rolesIds = new List<int>();

    public AdminPage()
    {
        InitializeComponent();
    }

    protected override async void OnAppearing()
    {
        base.OnAppearing();
        await CargarRoles();
    }

    private async Task CargarRoles()
    {
        try
        {
            using var conn = new SqlConnection(connectionString);
            await conn.OpenAsync();

            string query = "SELECT Id, NombreRol FROM Roles";
            using var cmd = new SqlCommand(query, conn);
            using var reader = await cmd.ExecuteReaderAsync();

            _rolesIds.Clear();
            var roles = new List<string>();
            while (await reader.ReadAsync())
            {
                _rolesIds.Add((int)reader["Id"]);
                roles.Add(reader["NombreRol"].ToString());
            }

            pickerRol.ItemsSource = roles;
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", $"No se pudieron cargar los roles: {ex.Message}", "OK");
        }
    }

    private async void OnLogoutClicked(object sender, EventArgs e) =>
        await Shell.Current.GoToAsync("//MainPage");

    private async void OnInsertClicked(object sender, EventArgs e) =>
        await EjecutarAccion(@"INSERT INTO Usuarios (Usuario, Password, IdRol) 
                               VALUES (@Usuario, CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', @Password), 2), @IdRol)", "insertar");

    private async void OnUpdateClicked(object sender, EventArgs e) =>
        await EjecutarAccion(@"UPDATE Usuarios 
                               SET Usuario=@Usuario, Password=CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', @Password), 2), IdRol=@IdRol 
                               WHERE Id=@Id", "actualizar");

    private async void OnDeleteClicked(object sender, EventArgs e) =>
        await EjecutarAccion("DELETE FROM Usuarios WHERE Id=@Id", "eliminar");

    private async Task EjecutarAccion(string query, string accion)
    {
        if (isProcessing) return;

        bool confirmar = await DisplayAlert("Confirmación", $"¿Seguro que desea {accion} este usuario?", "Sí", "No");
        if (!confirmar) return;

        if (pickerRol.SelectedIndex < 0)
        {
            await DisplayAlert("Error", "Debe seleccionar un rol.", "OK");
            return;
        }

        isProcessing = true;
        try
        {
            using var conn = new SqlConnection(connectionString);
            await conn.OpenAsync();

            using var cmd = new SqlCommand(query, conn);
            cmd.Parameters.AddWithValue("@Usuario", txtUsuario.Text ?? "");
            cmd.Parameters.AddWithValue("@Password", txtPassword.Text ?? "");

            cmd.Parameters.AddWithValue("@IdRol", _rolesIds[pickerRol.SelectedIndex]);
            cmd.Parameters.AddWithValue("@Id", idSeleccionado);

            await cmd.ExecuteNonQueryAsync();
            await DisplayAlert("Éxito", $"Usuario {accion}do correctamente.", "OK");

            LimpiarCampos();
            await CargarLista("SELECT U.Id, U.Usuario, R.NombreRol FROM Usuarios U INNER JOIN Roles R ON U.IdRol = R.Id", "");
        }
        catch (Exception ex) { await DisplayAlert("Error", ex.Message, "OK"); }
        finally { isProcessing = false; }
    }

    private async void OnConsultClicked(object sender, EventArgs e) =>
        await CargarLista(@"SELECT U.Id, U.Usuario, R.NombreRol 
                            FROM Usuarios U INNER JOIN Roles R ON U.IdRol = R.Id", "");

    private async void OnSearchChanged(object sender, TextChangedEventArgs e)
    {
        string filtro = "%" + e.NewTextValue + "%";
        string query = @"SELECT U.Id, U.Usuario, R.NombreRol 
                         FROM Usuarios U INNER JOIN Roles R ON U.IdRol = R.Id 
                         WHERE U.Usuario LIKE @Filtro OR CAST(U.Id AS VARCHAR) LIKE @Filtro";
        await CargarLista(query, filtro);
    }

    private async Task CargarLista(string query, string parametro)
    {
        try
        {
            using var conn = new SqlConnection(connectionString);
            await conn.OpenAsync();

            using var cmd = new SqlCommand(query, conn);
            if (!string.IsNullOrEmpty(parametro)) cmd.Parameters.AddWithValue("@Filtro", parametro);

            using var reader = await cmd.ExecuteReaderAsync();
            var lista = new List<UsuarioItem>();

            while (await reader.ReadAsync())
                lista.Add(new UsuarioItem
                {
                    Id = (int)reader["Id"],
                    Usuario = reader["Usuario"].ToString(),
                    Rol = reader["NombreRol"].ToString()
                });

            listaUsuarios.ItemsSource = lista;
        }
        catch (Exception ex) { await DisplayAlert("Error", ex.Message, "OK"); }
    }

    private void OnUsuarioSelected(object sender, SelectionChangedEventArgs e)
    {
        var item = e.CurrentSelection.FirstOrDefault() as UsuarioItem;
        if (item != null)
        {
            idSeleccionado = item.Id;
            txtUsuario.Text = item.Usuario;
            txtPassword.Text = "";

            if (pickerRol.ItemsSource is List<string> roles)
            {
                pickerRol.SelectedIndex = roles.IndexOf(item.Rol);
            }
        }
    }

    private async void OnValidateClicked(object sender, EventArgs e)
    {
        using var conn = new SqlConnection(connectionString);
        await conn.OpenAsync();

        string query = @"SELECT U.Usuario 
                         FROM Usuarios U 
                         WHERE U.Usuario=@U AND U.Password=CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', @P), 2)";

        using var cmd = new SqlCommand(query, conn);
        cmd.Parameters.AddWithValue("@U", txtUsuario.Text);
        cmd.Parameters.AddWithValue("@P", txtPassword.Text);

        lblMensaje.Text = (await cmd.ExecuteScalarAsync() != null) ? "✅ Credenciales correctas" : "❌ Incorrecto";
    }

    private void OnClearClicked(object sender, EventArgs e) => LimpiarCampos();

    private async void OnRolesClicked(object sender, EventArgs e)
    {
        await Navigation.PushAsync(new RolesPage());
    }

    private void LimpiarCampos()
    {
        idSeleccionado = 0;
        txtUsuario.Text = txtPassword.Text = txtBuscar.Text = "";
        pickerRol.SelectedIndex = -1;
        lblMensaje.Text = "";
        listaUsuarios.ItemsSource = null;
    }
}




``

---

## 🎭 PASO 5: Vistas (ROLES)

### 🧠 El Modelo (Models/RolItem.cs)

``csharp
namespace CRUD_LOGIN_MAUI.Models;

public class RolItem
{
    public int Id { get; set; }
    public string NombreRol { get; set; }
}
``

### 🎨 La Vista (Views/RolesPage.xaml)

``xml
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:local="clr-namespace:CRUD_LOGIN_MAUI.Views"
             xmlns:models="clr-namespace:CRUD_LOGIN_MAUI.Models"
             x:Class="CRUD_LOGIN_MAUI.Views.RolesPage"
             Title="Gestión de Roles">

    <ScrollView>
        <VerticalStackLayout Padding="20" Spacing="15" BackgroundColor="#FFFDE7">

            <Label Text="Panel de Control - Roles"
                   FontSize="22"
                   FontAttributes="Bold"
                   TextColor="#BF360C"
                   HorizontalOptions="Center"/>

            <!-- Campo para nombre del rol -->
            <Entry x:Name="txtRol" Placeholder="🛡️ Nombre del Rol"/>

            <!-- Buscador -->
            <Entry x:Name="txtBuscar"
                   Placeholder="🔎 Buscar por ID o Nombre..."
                   TextChanged="OnSearchChanged"
                   BackgroundColor="White"/>

            <!-- Botones CRUD -->
            <Grid ColumnDefinitions="*,*,*" RowDefinitions="Auto,Auto" ColumnSpacing="10" RowSpacing="10">
                <Button Grid.Row="0" Grid.Column="0" Text="➕ Insertar" BackgroundColor="Green" TextColor="White" Clicked="OnInsertClicked"/>
                <Button Grid.Row="0" Grid.Column="1" Text="🔄 Actualizar" BackgroundColor="DodgerBlue" TextColor="White" Clicked="OnUpdateClicked"/>
                <Button Grid.Row="0" Grid.Column="2" Text="🗑️ Eliminar" BackgroundColor="Red" TextColor="White" Clicked="OnDeleteClicked"/>
                <Button Grid.Row="1" Grid.Column="0" Text="🔍 Consultar" BackgroundColor="Orange" TextColor="White" Clicked="OnConsultClicked"/>
                <Button Grid.Row="1" Grid.Column="2" Text="🧹 Limpiar" BackgroundColor="Gray" TextColor="White" Clicked="OnClearClicked"/>
            </Grid>

            <!-- Lista de roles -->
            <CollectionView x:Name="listaRoles"
                            SelectionMode="Single"
                            SelectionChanged="OnRolSelected"
                            HeightRequest="250">
                <CollectionView.ItemTemplate>
                    <DataTemplate x:DataType="local:RolItem">
                        <Grid Padding="10" ColumnDefinitions="40, *">
                            <Label Grid.Column="0" Text="{Binding Id}" FontAttributes="Bold" TextColor="Blue"/>
                            <Label Grid.Column="1" Text="{Binding NombreRol}" FontAttributes="Bold"/>
                        </Grid>
                    </DataTemplate>
                </CollectionView.ItemTemplate>
            </CollectionView>

            <!-- Botón logout -->
            <Button Text="Cerrar sesión"
                    BackgroundColor="DarkRed"
                    TextColor="White"
                    Margin="0,20"
                    Clicked="OnLogoutClicked"/>
        </VerticalStackLayout>
    </ScrollView>
</ContentPage>


``

### 🧩 Lógica (Views/RolesPage.xaml.cs)

``csharp
using Microsoft.Data.SqlClient;
using System.Data;

using CRUD_LOGIN_MAUI.Controllers;

namespace CRUD_LOGIN_MAUI.Views;

public class RolItem
{
    public int Id { get; set; }
    public string NombreRol { get; set; }
}

public partial class RolesPage : ContentPage
{
    private string connectionString = Config.ConnectionString;
    private bool isProcessing = false;
    private int idSeleccionado = 0;

    public RolesPage() => InitializeComponent();

    private async void OnLogoutClicked(object sender, EventArgs e) =>
        await Shell.Current.GoToAsync("//MainPage");

    private async void OnInsertClicked(object sender, EventArgs e) =>
        await EjecutarAccion("INSERT INTO Roles (NombreRol) VALUES (@NombreRol)", "insertar");

    private async void OnUpdateClicked(object sender, EventArgs e) =>
        await EjecutarAccion("UPDATE Roles SET NombreRol=@NombreRol WHERE Id=@Id", "actualizar");

    private async void OnDeleteClicked(object sender, EventArgs e) =>
        await EjecutarAccion("DELETE FROM Roles WHERE Id=@Id", "eliminar");

    private async Task EjecutarAccion(string query, string accion)
    {
        if (isProcessing) return;

        bool confirmar = await DisplayAlert("Confirmaci�n", $"�Seguro que desea {accion} este rol?", "S�", "No");
        if (!confirmar) return;

        isProcessing = true;
        try
        {
            using var conn = new SqlConnection(connectionString);
            await conn.OpenAsync();

            using var cmd = new SqlCommand(query, conn);
            cmd.Parameters.AddWithValue("@NombreRol", txtRol.Text ?? "");
            cmd.Parameters.AddWithValue("@Id", idSeleccionado);

            await cmd.ExecuteNonQueryAsync();
            await DisplayAlert("�xito", $"Rol {accion}do correctamente.", "OK");

            LimpiarCampos();
            await CargarLista("SELECT Id, NombreRol FROM Roles", "");
        }
        catch (Exception ex) { await DisplayAlert("Error", ex.Message, "OK"); }
        finally { isProcessing = false; }
    }

    private async void OnConsultClicked(object sender, EventArgs e) =>
        await CargarLista("SELECT Id, NombreRol FROM Roles", "");

    private async void OnSearchChanged(object sender, TextChangedEventArgs e)
    {
        string filtro = "%" + e.NewTextValue + "%";
        string query = "SELECT Id, NombreRol FROM Roles WHERE NombreRol LIKE @Filtro OR CAST(Id AS VARCHAR) LIKE @Filtro";
        await CargarLista(query, filtro);
    }

    private async Task CargarLista(string query, string parametro)
    {
        try
        {
            using var conn = new SqlConnection(connectionString);
            await conn.OpenAsync();

            using var cmd = new SqlCommand(query, conn);
            if (!string.IsNullOrEmpty(parametro)) cmd.Parameters.AddWithValue("@Filtro", parametro);

            using var reader = await cmd.ExecuteReaderAsync();
            var lista = new List<RolItem>();

            while (await reader.ReadAsync())
                lista.Add(new RolItem
                {
                    Id = (int)reader["Id"],
                    NombreRol = reader["NombreRol"].ToString()
                });

            listaRoles.ItemsSource = lista;
        }
        catch (Exception ex) { await DisplayAlert("Error", ex.Message, "OK"); }
    }

    private void OnRolSelected(object sender, SelectionChangedEventArgs e)
    {
        var item = e.CurrentSelection.FirstOrDefault() as RolItem;
        if (item != null)
        {
            idSeleccionado = item.Id;
            txtRol.Text = item.NombreRol;
        }
    }

    private void OnClearClicked(object sender, EventArgs e) => LimpiarCampos();

    private void LimpiarCampos()
    {
        idSeleccionado = 0;
        txtRol.Text = txtBuscar.Text = "";
        listaRoles.ItemsSource = null;
    }
}


``

---

## 👔 PASO 6: Vista Limitada (Supervisor)

### 🎨 La Vista (Views/SupervisorPage.xaml)

``xml
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="CRUD_LOGIN_MAUI.Views.SupervisorPage"
             Title="SupervisorPage">
    <VerticalStackLayout Padding="30" Spacing="20" BackgroundColor="#FFF3E0">
        <Label Text="Bienvenido Supervisor"
               FontSize="24"
               FontAttributes="Bold"
               TextColor="#E65100"
               HorizontalOptions="Center" 
               Margin="10"/>

        <!-- Logo -->
        <Image Source="https://cdn-icons-png.flaticon.com/256/3461/3461567.png"
                 HeightRequest="175"
                 HorizontalOptions="Center" />

        <Label Text="Ventana: Reportes y supervision"
               FontSize="18"
               TextColor="Black"
               HorizontalOptions="Center" 
                Margin="10" />

        <Button Text="Cerrar Sesion" 
                Clicked="OnLogoutClicked" 
                BackgroundColor="#D32F2F" 
                TextColor="White" 
                HorizontalOptions="Center" 
                Margin="0,20,0,0" />
    </VerticalStackLayout>
</ContentPage>


``

### 🧩 Lógica (Views/SupervisorPage.xaml.cs)

``csharp
using CRUD_LOGIN_MAUI.Controllers;

namespace CRUD_LOGIN_MAUI.Views;

public partial class SupervisorPage : ContentPage
{
    public SupervisorPage()
    {
        InitializeComponent();
    }

    private async void OnLogoutClicked(object sender, EventArgs e)
    {
        await Shell.Current.GoToAsync("//MainPage");
    }
}


``

---

## 🛍️ PASO 7: Vista Limitada (Vendedor)

### 🎨 La Vista (Views/VendedorPage.xaml)

``xml
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             x:Class="CRUD_LOGIN_MAUI.Views.VendedorPage"
             Title="VendedorPage">
    <VerticalStackLayout Padding="30" Spacing="20" BackgroundColor="#E8F5E9">
        <Label Text="Bienvenido Vendedor"
               FontSize="24"
               FontAttributes="Bold"
               TextColor="#1B5E20"
               HorizontalOptions="Center"
               Margin="10"/>

        <!-- Logo -->
        <Image Source="https://cdn-icons-png.flaticon.com/512/2316/2316167.png"
                 HeightRequest="175"
                 HorizontalOptions="Center" />

        <Label Text="Ventana: Modulo de ventas"
               FontSize="18"
               TextColor="Black"
               HorizontalOptions="Center"
                Margin="10"/>

        <Button Text="Cerrar Sesion" 
                Clicked="OnLogoutClicked" 
                BackgroundColor="#D32F2F" 
                TextColor="White" 
                HorizontalOptions="Center" 
                Margin="0,20,0,0" />
    </VerticalStackLayout>
</ContentPage>


``

### 🧩 Lógica (Views/VendedorPage.xaml.cs)

``csharp
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


``

---

## ✅ Conclusión

¡Felicidades! 🎉 Has reestructurado exitosamente una aplicación de .NET MAUI monolítica a un sistema organizado bajo el **patrón de diseño MVC**.

Esto no solo hace que tu proyecto sea más profesional y ordenado (Modelos separados de las Vistas y Controladores aislados), sino que además permite que tu código sea **mantenible en el tiempo**. Tienes seguridad, bases de datos reales y una arquitectura de primer nivel sin perder simplicidad.
