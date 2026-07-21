$proj = "C:\Users\User\Desktop\CRUD_LOGIN_MAUI_MVC\CRUD_LOGIN_MAUI"
cd $proj

New-Item -ItemType Directory -Force -Path Models, Views, Controllers

Move-Item Config.cs Controllers\
Move-Item MainPage.xaml, MainPage.xaml.cs Views\
Move-Item AdminPage.xaml, AdminPage.xaml.cs Views\
Move-Item RolesPage.xaml, RolesPage.xaml.cs Views\
Move-Item SupervisorPage.xaml, SupervisorPage.xaml.cs Views\
Move-Item VendedorPage.xaml, VendedorPage.xaml.cs Views\

# Extract UsuarioItem
$usuarioItemCode = @"
namespace CRUD_LOGIN_MAUI.Models;

public class UsuarioItem
{
    public int Id { get; set; }
    public string Usuario { get; set; }
    public string Rol { get; set; }
}
"@
Set-Content -Path Models\UsuarioItem.cs -Value $usuarioItemCode

# Fix namespaces in Config
(Get-Content Controllers\Config.cs) -replace 'namespace CRUD_LOGIN_MAUI;', 'namespace CRUD_LOGIN_MAUI.Controllers;' | Set-Content Controllers\Config.cs

# Fix AdminPage (remove UsuarioItem class and update namespace)
$adminPageCs = Get-Content Views\AdminPage.xaml.cs -Raw
$adminPageCs = $adminPageCs -replace '(?s)public class UsuarioItem.*?\}', ''
$adminPageCs = $adminPageCs -replace 'namespace CRUD_LOGIN_MAUI;', "using CRUD_LOGIN_MAUI.Controllers;`nusing CRUD_LOGIN_MAUI.Models;`n`nnamespace CRUD_LOGIN_MAUI.Views;"
Set-Content -Path Views\AdminPage.xaml.cs -Value $adminPageCs

# Fix other Views namespaces and add Controllers using
Get-ChildItem -Path Views -Filter *.cs | Where-Object { $_.Name -ne 'AdminPage.xaml.cs' } | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $content = $content -replace 'namespace CRUD_LOGIN_MAUI;', "using CRUD_LOGIN_MAUI.Controllers;`n`nnamespace CRUD_LOGIN_MAUI.Views;"
    Set-Content -Path $_.FullName -Value $content
}

# Fix XAML files
Get-ChildItem -Path Views -Filter *.xaml | ForEach-Object {
    (Get-Content $_.FullName) -replace 'x:Class="CRUD_LOGIN_MAUI.', 'x:Class="CRUD_LOGIN_MAUI.Views.' | Set-Content $_.FullName
}

# Update AppShell.xaml
$appShellXaml = Get-Content AppShell.xaml -Raw
$appShellXaml = $appShellXaml -replace 'xmlns:local="clr-namespace:CRUD_LOGIN_MAUI"', "xmlns:local=`"clr-namespace:CRUD_LOGIN_MAUI`"`n    xmlns:views=`"clr-namespace:CRUD_LOGIN_MAUI.Views`""
$appShellXaml = $appShellXaml -replace 'local:', 'views:'
Set-Content -Path AppShell.xaml -Value $appShellXaml

# Update AppShell.xaml.cs
$appShellCs = Get-Content AppShell.xaml.cs -Raw
$appShellCs = $appShellCs -replace 'namespace CRUD_LOGIN_MAUI;', "using CRUD_LOGIN_MAUI.Views;`n`nnamespace CRUD_LOGIN_MAUI;"
Set-Content -Path AppShell.xaml.cs -Value $appShellCs

