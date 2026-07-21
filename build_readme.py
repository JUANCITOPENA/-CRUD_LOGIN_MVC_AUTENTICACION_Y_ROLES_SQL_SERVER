import os
import re

old_readme_path = r'C:\Users\User\Downloads\README (3).md'
new_readme_path = r'C:\Users\User\Desktop\CRUD_LOGIN_MAUI_MVC\README.md'
proj_path = r'C:\Users\User\Desktop\CRUD_LOGIN_MAUI_MVC\CRUD_LOGIN_MAUI'

def get_file(rel_path):
    with open(os.path.join(proj_path, rel_path), 'r', encoding='utf-8') as f:
        return f.read().strip()

with open(old_readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Title and Add MVC Context
content = content.replace(
    '# 🔐 CRUD_LOGIN_MAUI — Sistema de Autenticación y Roles con .NET MAUI + SQL Server',
    '# 🔐 CRUD_LOGIN_MAUI — Sistema de Autenticación y Roles con .NET MAUI + SQL Server (Versión MVC)'
)

mvc_intro = '''
## 🧠 ¿Por qué MVC y no el código anterior?

En la versión anterior de este proyecto, teníamos una arquitectura "monolítica" (también conocida como *Code-Behind* pesado). Las clases de datos, la configuración de la base de datos y el diseño visual vivían amontonados.

Al evolucionar a **MVC (Modelo-Vista-Controlador)** de manera sencilla, separamos responsabilidades:
- **Models (Modelos):** Aquí viven nuestras clases de datos (ej. UsuarioItem.cs, RolItem.cs). Representan la información pura.
- **Views (Vistas):** Contienen exclusivamente las pantallas (.xaml y .xaml.cs). Su único trabajo es mostrar la interfaz al usuario.
- **Controllers (Controladores):** Alojan la configuración, la cadena de conexión (Config.cs) y orquestan la base de datos. 

**¿Por qué es mejor?**
1. **Orden:** Sabes exactamente dónde encontrar cada cosa. Si falla el diseño, vas a *Views*. Si falla la conexión, vas a *Controllers*.
2. **Reutilización:** Las clases de los *Models* pueden ser usadas por varias pantallas sin tener que reescribirlas dentro de cada .xaml.cs.
3. **Escalabilidad Sencilla:** Te permite tener un proyecto muy profesional y limpio sin llegar a la extrema complejidad del patrón MVVM (Model-View-ViewModel), manteniendo la narrativa directa que ya conoces.

'''
content = content.replace('## 🧭 Visión General del Proyecto', mvc_intro + '## 🧭 Visión General del Proyecto')

# 2. Update folder structure block
old_folder = '''📁 CRUD_LOGIN_MAUI
 ├── 📁 Dependencies            # 📦 Paquetes (Microsoft.Data.SqlClient)
 ├── 📁 Platforms               # 🤖 Código específico por plataforma (Android, iOS, Windows)
 ├── 📁 Resources               # 🎨 Recursos visuales (AppIcon, Fonts, Images, Styles)
 │
 ├── 📄 App.xaml                # 🖌️ Diccionarios de recursos y estilos globales
 ├── 📄 App.xaml.cs             # 🚀 Punto de entrada (Llama al AppShell)
 ├── 📄 AppShell.xaml           # 🗺️ Enrutador visual (Gestor de las rutas base)
 ├── 📄 AppShell.xaml.cs        # 🔗 Registro de rutas ocultas mediante C#
 │
 ├── 📄 MainPage.xaml           # 🚪 Pantalla principal de Acceso (Login)
 ├── 📄 AdminPage.xaml          # 👑 Panel del Administrador (CRUD Usuarios)
 ├── 📄 RolesPage.xaml          # 🎭 Gestión del catálogo de roles (CRUD Roles)
 ├── 📄 SupervisorPage.xaml     # 👔 Vista limitada a reportes y supervisión
 ├── 📄 VendedorPage.xaml       # 🛍️ Vista operativa para módulo de ventas
 │
 ├── 📄 MauiProgram.cs          # ⚙️ Inyector de dependencias y fuentes de MAUI
 └── 📄 CRUD_LOGIN_MAUI.csproj  # 🏗️ Archivo maestro (net9.0 y reglas de nulos)'''

new_folder = '''📁 CRUD_LOGIN_MAUI
 ├── 📁 Dependencies            # 📦 Paquetes (Microsoft.Data.SqlClient)
 ├── 📁 Platforms               # 🤖 Código específico por plataforma (Android, iOS, Windows)
 ├── 📁 Resources               # 🎨 Recursos visuales (AppIcon, Fonts, Images, Styles)
 │
 ├── 📁 Models                  # 🧠 MODELOS (Datos puros)
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
 ├── 📁 Controllers             # ⚙️ CONTROLADORES (Configuración y Lógica central)
 │    └── 📄 Config.cs          
 │
 ├── 📄 App.xaml / .cs          # 🖌️ Diccionarios de recursos y estilos globales
 ├── 📄 AppShell.xaml / .cs     # 🗺️ Enrutador visual (Gestor de las rutas base)
 ├── 📄 MauiProgram.cs          # ⚙️ Inyector de dependencias y fuentes de MAUI
 └── 📄 CRUD_LOGIN_MAUI.csproj  # 🏗️ Archivo maestro (net9.0 y reglas de nulos)'''

content = content.replace(old_folder, new_folder)

# Function to replace code block
def replace_code_block(content, marker_start, marker_end, new_code, lang='csharp'):
    pattern = re.compile(re.escape(marker_start) + r'.*?' + re.escape(marker_end), re.DOTALL)
    replacement = marker_start + '\n`' + lang + '\n' + new_code + '\n`\n\n' + marker_end
    return pattern.sub(replacement, content)

# 3. Replace App.xaml.cs
content = replace_code_block(content,
    "**App.xaml.cs** (Lógica de inicialización):",
    "### 📄 ¿Cómo editar el archivo AppShell.xaml?",
    get_file('App.xaml.cs'), 'csharp')

# 4. Replace AppShell.xaml
content = replace_code_block(content,
    "reemplaza su contenido por este. Hemos desactivado el menú lateral (FlyoutBehavior=\"Disabled\") para forzar que la navegación ocurra **solo** a través de botones y lógica de código — evitando que el usuario acceda manualmente a pantallas de otros roles.",
    "### ⚙️ ¿Cómo editar el archivo AppShell.xaml.cs?",
    get_file('AppShell.xaml'), 'xml')

# 5. Replace AppShell.xaml.cs
content = replace_code_block(content,
    "sino registrada manualmente para navegación por *push* (Navigation.PushAsync).",
    "> 💡 **Tip:** El nombre del rol devuelto por la consulta SQL",
    get_file('AppShell.xaml.cs'), 'csharp')

# 6. Replace MainPage.xaml
content = replace_code_block(content,
    "ojito\" para mostrar/ocultar la contraseña temporalmente.",
    "### ⚙️ Centralizar la Conexión (Config.cs)",
    get_file(r'Views\MainPage.xaml'), 'xml')

# 7. Replace Config.cs
content = replace_code_block(content,
    "3. Pega el siguiente código:",
    "### 🧠 ¿Cómo editar el archivo MainPage.xaml.cs (La Lógica)?",
    get_file(r'Controllers\Config.cs'), 'csharp')

# 8. Replace MainPage.xaml.cs
content = replace_code_block(content,
    "para redirigir dinámicamente (AdminPage, VendedorPage, etc).",
    "> 🛡️ **Buena práctica aplicada:** la consulta usa **parámetros SQL**",
    get_file(r'Views\MainPage.xaml.cs'), 'csharp')

# 9. AdminPage XAML
content = replace_code_block(content,
    "Se usa para la gestión completa (CRUD) de los usuarios, e incluye un buscador en tiempo real y una lista (CollectionView) con *compiled bindings*.",
    "### 🧩 Lógica de Ejecución Centralizada (AdminPage.xaml.cs)",
    get_file(r'Views\AdminPage.xaml'), 'xml')

# 10. AdminPage.xaml.cs and UsuarioItem.cs
admin_logic = get_file(r'Models\UsuarioItem.cs') + '\n\n' + get_file(r'Views\AdminPage.xaml.cs')
content = replace_code_block(content,
    "encapsula la apertura de conexión, ejecución y recarga de la lista.",
    "> 📝 **Detalle importante:** al actualizar un usuario, el campo de contraseña",
    admin_logic, 'csharp')

# 11. RolesPage.xaml
content = replace_code_block(content,
    "### 📄 RolesPage.xaml (Gestión del Catálogo de Roles)",
    "### ⚙️ RolesPage.xaml.cs (Lógica del Catálogo de Roles)",
    get_file(r'Views\RolesPage.xaml'), 'xml')

# 12. RolesPage.xaml.cs and RolItem.cs
roles_logic = get_file(r'Models\RolItem.cs') + '\n\n' + get_file(r'Views\RolesPage.xaml.cs')
content = replace_code_block(content,
    "### ⚙️ RolesPage.xaml.cs (Lógica del Catálogo de Roles)",
    "> ⚠️ **Cuidado con la integridad referencial:** al eliminar un rol",
    roles_logic, 'csharp')

# 13. SupervisorPage.xaml
content = replace_code_block(content,
    "### 📄 SupervisorPage.xaml (Pantalla Restringida)",
    "### ⚙️ SupervisorPage.xaml.cs (Lógica Restringida)",
    get_file(r'Views\SupervisorPage.xaml'), 'xml')

# 14. SupervisorPage.xaml.cs
content = replace_code_block(content,
    "### ⚙️ SupervisorPage.xaml.cs (Lógica Restringida)",
    "> 💡 **Idea de extensión:** este espacio (\"Ventana: Reportes y supervisión\")",
    get_file(r'Views\SupervisorPage.xaml.cs'), 'csharp')

# 15. VendedorPage.xaml
content = replace_code_block(content,
    "### 📄 VendedorPage.xaml (Pantalla Restringida)",
    "### ⚙️ VendedorPage.xaml.cs (Lógica Restringida)",
    get_file(r'Views\VendedorPage.xaml'), 'xml')

# 16. VendedorPage.xaml.cs
content = replace_code_block(content,
    "### ⚙️ VendedorPage.xaml.cs (Lógica Restringida)",
    "> 💡 **Idea de extensión:** el \"Módulo de ventas\" es el lugar",
    get_file(r'Views\VendedorPage.xaml.cs'), 'csharp')

# Fix instructions about creating files
content = content.replace(
    'Abre AppShell.xaml y reemplaza su contenido por este.',
    'Abre AppShell.xaml y reemplaza su contenido por este (nota el uso de xmlns:views).'
)
content = content.replace(
    'Crea la clase estática Config.cs en la raíz del proyecto.',
    'Crea una carpeta llamada Controllers en la raíz del proyecto y dentro de ella crea la clase estática Config.cs.'
)
content = content.replace(
    '1. Clic derecho en el proyecto → **Add** → **Class...**\n2. Nómbrala Config.cs.',
    '1. Crea la carpeta Controllers.\n2. Clic derecho en Controllers → **Add** → **Class...**\n3. Nómbrala Config.cs.'
)
content = content.replace(
    '4. Visual Studio generará automáticamente AdminPage.xaml y su code-behind AdminPage.xaml.cs.',
    '4. Visual Studio generará automáticamente AdminPage.xaml y su code-behind AdminPage.xaml.cs. Mueve estos archivos a la carpeta Views (o créalos directamente allí) y crea el modelo UsuarioItem.cs en la carpeta Models.'
)

with open(new_readme_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done generating README.")
