# 🔐 CRUD_LOGIN_MAUI — Sistema de Autenticación y Roles (Versión MVC)

> 📘 **Manual paso a paso, completo y documentado**
> Guía exhaustiva para construir (o entender) un sistema de **login con roles** desarrollado en **.NET MAUI**, con conexión directa a **SQL Server**, contraseñas protegidas mediante **hashing SHA2_256** y estructurado con el **Patrón MVC (Modelo-Vista-Controlador)**.

---

## 📑 Tabla de Contenidos

| # | Paso | Descripción |
|---|------|-------------|
| 🧠 | [Contexto MVC](#-por-qué-mvc-y-no-el-código-anterior) | Teoría y ventajas de la arquitectura MVC |
| 🗄️ | [Paso 1](#️-paso-1-configurar-la-base-de-datos-sql-server) | Configurar la Base de Datos (SQL Server) |
| 🚀 | [Paso 2](#-paso-2-enrutamiento-principal-appshell) | Enrutamiento Principal (`AppShell`) |
| 🔒 | [Paso 3](#-paso-3-pantalla-de-login-mainpage) | Pantalla de Login (`MainPage`) |
| 🛠️ | [Paso 4](#️-paso-4-panel-de-control-adminpage) | Panel de Control (`AdminPage`) |
| 🎭 | [Paso 5](#-paso-5-vistas-roles) | Vista de Gestión de Roles |
| 👔 | [Paso 6](#-paso-6-vistas-limitadas-supervisor) | Vista Restringida — Supervisor |
| 🛍️ | [Paso 7](#️-paso-7-vistas-limitadas-vendedor) | Vista Restringida — Vendedor |
| ✅ | [Cierre](#-conclusión) | Conclusión y buenas prácticas |

---

## 🧠 ¿Por qué MVC y no el código anterior?

En la versión anterior de este proyecto, teníamos una arquitectura "monolítica" (también conocida como *Code-Behind* pesado). Las clases de datos, la configuración de la base de datos y el diseño visual vivían amontonados.

Al evolucionar a **MVC (Modelo-Vista-Controlador)** de manera sencilla, separamos responsabilidades:
- **Models (Modelos):** Aquí viven nuestras clases de datos (ej. `UsuarioItem.cs`, `RolItem.cs`). Representan la información pura.
- **Views (Vistas):** Contienen exclusivamente las pantallas (`.xaml` y `.xaml.cs`). Su único trabajo es mostrar la interfaz al usuario.
- **Controllers (Controladores):** Alojan la configuración, la cadena de conexión (`Config.cs`) y orquestan la base de datos. 

**¿Por qué es mejor?**
1. **Orden:** Sabes exactamente dónde encontrar cada cosa. Si falla el diseño, vas a *Views*. Si falla la conexión, vas a *Controllers*.
2. **Reutilización:** Las clases de los *Models* pueden ser usadas por varias pantallas sin tener que reescribirlas dentro de cada `.xaml.cs`.
3. **Escalabilidad Sencilla:** Te permite tener un proyecto muy profesional y limpio sin llegar a la extrema complejidad del patrón MVVM (Model-View-ViewModel), manteniendo la narrativa directa que ya conoces.

---

## 🧭 Visión General del Proyecto

Este proyecto es un **sistema educativo de autenticación con roles** (Admin, Supervisor, Vendedor) que demuestra un flujo completo usando MVC:

- 🔑 **Login seguro** validado contra SQL Server con contraseñas encriptadas (nunca en texto plano).
- 🧩 **Navegación basada en Shell**, redirigiendo dinámicamente según el rol.
- 🗂️ **CRUD completo** de usuarios y roles desde la app (Insertar, Actualizar, Eliminar, Consultar, Validar).
- 🎨 **Vistas diferenciadas por rol**, donde solo el Administrador tiene permisos de escritura.

```text
📁 CRUD_LOGIN_MAUI
 ├── 📁 Dependencies            
 ├── 📁 Platforms               
 ├── 📁 Resources               
 │
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
 ├── 📁 Controllers             # ⚙️ CONTROLADORES (Configuración/Lógica central)
 │    └── 📄 Config.cs          
 │
 ├── 📄 App.xaml / .cs          
 ├── 📄 AppShell.xaml / .cs     
 ├── 📄 MauiProgram.cs          
 └── 📄 CRUD_LOGIN_MAUI.csproj  
```

### 🧰 Requisitos previos

| Herramienta | Uso |
|---|---|
| 🖥️ Visual Studio 2022 (17.8+) | Crear y ejecutar el proyecto MAUI |
| 🗃️ SQL Server (Express, Developer) | Alojar la base de datos `LoginRolesDB_cif` |
| 🧩 SSMS | Ejecutar scripts y administrar la base de datos |
| 📦 `Microsoft.Data.SqlClient` | Conectar la app MAUI con SQL Server |

---

## 🗄️ PASO 1: Configurar la Base de Datos (SQL Server)

*(La configuración de SQL Server es idéntica a la versión anterior. Si ya ejecutaste el script y configuraste tu IP/Puerto 1433, puedes omitir esto)*.

### 📜 Script completo de creación de la base de datos

```sql
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
    Password VARCHAR(64) NOT NULL, -- HASH SHA2_256
    IdRol INT FOREIGN KEY REFERENCES Roles(Id)
);

INSERT INTO Roles (NombreRol) VALUES ('Admin'), ('Supervisor'), ('Vendedor');

INSERT INTO Usuarios (Usuario, Password, IdRol) VALUES
('AdminUser', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'admin123'), 2), 1),
('SuperUser', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'super123'), 2), 2),
('SalesUser', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'sales123'), 2), 3);
GO
```

---

## 🚀 PASO 2: Enrutamiento Principal (`AppShell`)

En la arquitectura MVC, debemos avisarle a `AppShell` dónde viven nuestras vistas.

### 🛠️ Inicialización Base (`App.xaml.cs`)

```csharp
using Microsoft.Extensions.DependencyInjection;
using CRUD_LOGIN_MAUI.Views; // Importamos la carpeta Views

namespace CRUD_LOGIN_MAUI;

public partial class App : Application
{
	public App()
	{
		InitializeComponent();
	}

	protected override Window CreateWindow(IActivationState? activationState) // Nota: Nulabilidad corregida
	{
		return new Window(new AppShell());
	}
}
```

### 📄 Editar el archivo `AppShell.xaml`

Agregamos el `xmlns:views` para que el XAML sepa buscar las páginas dentro de la carpeta `Views`.

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<Shell
    x:Class="CRUD_LOGIN_MAUI.AppShell"
    xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
    xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
    xmlns:views="clr-namespace:CRUD_LOGIN_MAUI.Views"
    Title="CRUD_LOGIN_MAUI"
    FlyoutBehavior="Disabled">

    <ShellContent
        Title="Home"
        ContentTemplate="{DataTemplate views:MainPage}"
        Route="MainPage" />

    <ShellContent Route="AdminPage" ContentTemplate="{DataTemplate views:AdminPage}" FlyoutItem.IsVisible="False"/>
    <ShellContent Route="SupervisorPage" ContentTemplate="{DataTemplate views:SupervisorPage}" FlyoutItem.IsVisible="False"/>
    <ShellContent Route="VendedorPage" ContentTemplate="{DataTemplate views:VendedorPage}" FlyoutItem.IsVisible="False"/>
</Shell>
```

### ⚙️ Archivo `AppShell.xaml.cs`

```csharp
using CRUD_LOGIN_MAUI.Views; // Importante para reconocer las páginas

namespace CRUD_LOGIN_MAUI;

public partial class AppShell : Shell
{
    public AppShell()
    {
        InitializeComponent();
        
        Routing.RegisterRoute("AdminPage", typeof(AdminPage));
        Routing.RegisterRoute("SupervisorPage", typeof(SupervisorPage));
        Routing.RegisterRoute("VendedorPage", typeof(VendedorPage));
        Routing.RegisterRoute("RolesPage", typeof(RolesPage));
    }
}
```

---

## 🔒 PASO 3: Pantalla de Login (`MainPage`)

Crea la carpeta `Views` y coloca ahí `MainPage.xaml`. 

### ⚙️ Centralizar la Conexión (`Config.cs` en `Controllers`)

Crea la carpeta `Controllers` y agrega `Config.cs`. Al estar aquí, separamos la lógica pura de conexión de las pantallas.

```csharp
namespace CRUD_LOGIN_MAUI.Controllers;

public static class Config
{
    public const string ConnectionString = "Server=10.0.0.15,1433;Database=LoginRolesDB_cif;User Id=JUANCITO;Password=123456;TrustServerCertificate=True;";
}
```

### 🧠 Lógica de `Views/MainPage.xaml.cs`

Asegúrate de importar el controlador.

```csharp
using Microsoft.Data.SqlClient;
using System.Data;
using CRUD_LOGIN_MAUI.Controllers; // Referencia al controlador

namespace CRUD_LOGIN_MAUI.Views; // Nota el namespace .Views

public partial class MainPage : ContentPage
{
    public MainPage()
    {
        InitializeComponent();
    }

    // ... (El resto de la lógica de OnLogin_Clicked se mantiene igual usando Config.ConnectionString)
```

---

## 🛠️ PASO 4: Panel de Control (`AdminPage`)

### 🧠 El Modelo (`Models/UsuarioItem.cs`)

En lugar de tener la clase dentro de `AdminPage`, la separamos a la carpeta `Models`.

```csharp
namespace CRUD_LOGIN_MAUI.Models;

public class UsuarioItem
{
    public int Id { get; set; }
    public string Usuario { get; set; }
    public string Rol { get; set; }
}
```

### 🎨 La Vista (`Views/AdminPage.xaml`)

Avisamos al XAML que use `xmlns:models` para encontrar el `DataType`.

```xml
<?xml version="1.0" encoding="utf-8" ?>
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:views="clr-namespace:CRUD_LOGIN_MAUI.Views"
             xmlns:models="clr-namespace:CRUD_LOGIN_MAUI.Models"
             x:Class="CRUD_LOGIN_MAUI.Views.AdminPage"
             Title="Administrador">

    <!-- ... (resto del diseño) -->
    
    <CollectionView x:Name="listaUsuarios" SelectionMode="Single" SelectionChanged="OnUsuarioSelected">
        <CollectionView.ItemTemplate>
            <DataTemplate x:DataType="models:UsuarioItem"> <!-- Apunta al modelo MVC -->
                <!-- ... bindings -->
            </DataTemplate>
        </CollectionView.ItemTemplate>
    </CollectionView>

</ContentPage>
```

### 🧩 Lógica (`Views/AdminPage.xaml.cs`)

```csharp
using Microsoft.Data.SqlClient;
using System.Data;
using CRUD_LOGIN_MAUI.Controllers;
using CRUD_LOGIN_MAUI.Models;

namespace CRUD_LOGIN_MAUI.Views;

public partial class AdminPage : ContentPage
{
    private string connectionString = Config.ConnectionString; // Viene del Controller
    // ... Todo el CRUD se mantiene exactamente igual.
```

---

## 🎭 PASO 5: Vistas (ROLES)

Igual que con los usuarios, crearemos `Models/RolItem.cs`.

```csharp
namespace CRUD_LOGIN_MAUI.Models;

public class RolItem
{
    public int Id { get; set; }
    public string NombreRol { get; set; }
}
```

Y en `Views/RolesPage.xaml`, usamos `models:RolItem` en nuestro `DataTemplate`. La lógica en `RolesPage.xaml.cs` usará `using CRUD_LOGIN_MAUI.Models;` y `using CRUD_LOGIN_MAUI.Controllers;`.

---

## 👔 PASO 6 & 7: Vistas Limitadas (Supervisor y Vendedor)

Para `Views/SupervisorPage.xaml.cs` y `Views/VendedorPage.xaml.cs`, el único cambio radical es asegurarte de que están envueltas en el namespace correcto:

```csharp
namespace CRUD_LOGIN_MAUI.Views;

public partial class SupervisorPage : ContentPage
{
    // ...
}
```

Y en el `.xaml`:
```xml
x:Class="CRUD_LOGIN_MAUI.Views.SupervisorPage"
```

---

## 🧱 Buenas Prácticas y Consideraciones Adicionales

| Área | Recomendación en Arquitectura MVC |
|---|---|
| 📂 **Orden** | Siempre que crees una tabla nueva en SQL, crea su clase gemela en la carpeta `Models`. |
| ⚙️ **Conexiones** | Si el día de mañana cambias de SQL Server a MySQL, solo tocas la carpeta `Controllers`, las Vistas quedan intactas. |
| 🌐 **Escalabilidad** | Gracias al MVC, cuando este proyecto crezca, podrás agregar *Servicios* y *Repositorios* a tu carpeta `Controllers` de forma natural. |

---

## ✅ Conclusión

¡Felicidades! 🎉 Has reestructurado exitosamente una aplicación de .NET MAUI monolítica a un sistema organizado bajo el **patrón de diseño MVC**.

Esto no solo hace que tu proyecto sea más profesional y ordenado (Modelos separados de las Vistas y Controladores aislados), sino que además permite que tu código sea **mantenible en el tiempo**. Tienes seguridad, bases de datos reales y una arquitectura de primer nivel sin perder simplicidad.