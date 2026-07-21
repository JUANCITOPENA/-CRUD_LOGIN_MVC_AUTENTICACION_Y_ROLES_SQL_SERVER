const fs = require('fs');
const path = require('path');

const oldReadmePath = 'C:\\Users\\User\\Downloads\\README (3).md';
const newReadmePath = 'C:\\Users\\User\\Desktop\\CRUD_LOGIN_MAUI_MVC\\README.md';
const projPath = 'C:\\Users\\User\\Desktop\\CRUD_LOGIN_MAUI_MVC\\CRUD_LOGIN_MAUI';

function getFile(relPath) {
    return fs.readFileSync(path.join(projPath, relPath), 'utf8').trim();
}

let content = fs.readFileSync(oldReadmePath, 'utf8');

content = content.replace(
    '# 🔐 CRUD_LOGIN_MAUI — Sistema de Autenticación y Roles con .NET MAUI + SQL Server',
    '# 🔐 CRUD_LOGIN_MAUI — Sistema de Autenticación y Roles con .NET MAUI + SQL Server (Versión MVC)'
);

const mvcIntro = `## 🧠 ¿Por qué MVC y no el código anterior?

En la versión anterior de este proyecto, teníamos una arquitectura "monolítica" (también conocida como *Code-Behind* pesado). Las clases de datos, la configuración de la base de datos y el diseño visual vivían amontonados.

Al evolucionar a **MVC (Modelo-Vista-Controlador)** de manera sencilla, separamos responsabilidades:
- **Models (Modelos):** Aquí viven nuestras clases de datos (ej. \`UsuarioItem.cs\`, \`RolItem.cs\`). Representan la información pura.
- **Views (Vistas):** Contienen exclusivamente las pantallas (\`.xaml\` y \`.xaml.cs\`). Su único trabajo es mostrar la interfaz al usuario.
- **Controllers (Controladores):** Alojan la configuración, la cadena de conexión (\`Config.cs\`) y orquestan la base de datos. 

**¿Por qué es mejor?**
1. **Orden:** Sabes exactamente dónde encontrar cada cosa. Si falla el diseño, vas a *Views*. Si falla la conexión, vas a *Controllers*.
2. **Reutilización:** Las clases de los *Models* pueden ser usadas por varias pantallas sin tener que reescribirlas dentro de cada \`.xaml.cs\`.
3. **Escalabilidad Sencilla:** Te permite tener un proyecto muy profesional y limpio sin llegar a la extrema complejidad del patrón MVVM (Model-View-ViewModel), manteniendo la narrativa directa que ya conoces.

`;
content = content.replace('## 🧭 Visión General del Proyecto', mvcIntro + '## 🧭 Visión General del Proyecto');

const oldFolder = `📁 CRUD_LOGIN_MAUI
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
 └── 📄 CRUD_LOGIN_MAUI.csproj  # 🏗️ Archivo maestro (net9.0 y reglas de nulos)`;

const newFolder = `📁 CRUD_LOGIN_MAUI
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
 └── 📄 CRUD_LOGIN_MAUI.csproj  # 🏗️ Archivo maestro (net9.0 y reglas de nulos)`;

content = content.replace(oldFolder, newFolder);

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); 
}

function replaceCodeBlock(content, markerStart, markerEnd, newCode, lang) {
    const pattern = new RegExp(escapeRegExp(markerStart) + '[\\s\\S]*?' + escapeRegExp(markerEnd));
    const replacement = markerStart + '\n```' + lang + '\n' + newCode + '\n```\n\n' + markerEnd;
    return content.replace(pattern, replacement);
}

content = replaceCodeBlock(content,
    "**`App.xaml.cs`** (Lógica de inicialización):\\n> ⚠️ **Importante:** Al tener desactivadas las advertencias de nulos globales, removemos el signo `?` de `IActivationState` que viene por defecto.",
    "### 📄 ¿Cómo editar el archivo `AppShell.xaml`?",
    getFile('App.xaml.cs'), 'csharp');

content = replaceCodeBlock(content,
    "reemplaza su contenido por este. Hemos desactivado el menú lateral (`FlyoutBehavior=\"Disabled\"`) para forzar que la navegación ocurra **solo** a través de botones y lógica de código — evitando que el usuario acceda manualmente a pantallas de otros roles.",
    "### ⚙️ ¿Cómo editar el archivo `AppShell.xaml.cs`?",
    getFile('AppShell.xaml'), 'xml');

content = replaceCodeBlock(content,
    "sino registrada manualmente para navegación por *push* (`Navigation.PushAsync`).",
    "> 💡 **Tip:** El nombre del rol devuelto por la consulta SQL",
    getFile('AppShell.xaml.cs'), 'csharp');

content = replaceCodeBlock(content,
    "ojito\" para mostrar/ocultar la contraseña temporalmente.",
    "### ⚙️ Centralizar la Conexión (`Config.cs`)",
    getFile('Views\\\\MainPage.xaml'), 'xml');

content = replaceCodeBlock(content,
    "3. Pega el siguiente código:",
    "### 🧠 ¿Cómo editar el archivo `MainPage.xaml.cs` (La Lógica)?",
    getFile('Controllers\\\\Config.cs'), 'csharp');

content = replaceCodeBlock(content,
    "para redirigir dinámicamente (`AdminPage`, `VendedorPage`, etc).",
    "> 🛡️ **Buena práctica aplicada:** la consulta usa **parámetros SQL**",
    getFile('Views\\\\MainPage.xaml.cs'), 'csharp');

content = replaceCodeBlock(content,
    "Se usa para la gestión completa (CRUD) de los usuarios, e incluye un buscador en tiempo real y una lista (`CollectionView`) con *compiled bindings*.",
    "### 🧩 Lógica de Ejecución Centralizada (`AdminPage.xaml.cs`)",
    getFile('Views\\\\AdminPage.xaml'), 'xml');

const adminLogic = getFile('Models\\\\UsuarioItem.cs') + '\n\n' + getFile('Views\\\\AdminPage.xaml.cs');
content = replaceCodeBlock(content,
    "encapsula la apertura de conexión, ejecución y recarga de la lista.",
    "> 📝 **Detalle importante:** al actualizar un usuario, el campo de contraseña",
    adminLogic, 'csharp');

content = replaceCodeBlock(content,
    "### 📄 `RolesPage.xaml` (Gestión del Catálogo de Roles)",
    "### ⚙️ `RolesPage.xaml.cs` (Lógica del Catálogo de Roles)",
    getFile('Views\\\\RolesPage.xaml'), 'xml');

const rolesLogic = getFile('Models\\\\RolItem.cs') + '\n\n' + getFile('Views\\\\RolesPage.xaml.cs');
content = replaceCodeBlock(content,
    "### ⚙️ `RolesPage.xaml.cs` (Lógica del Catálogo de Roles)",
    "> ⚠️ **Cuidado con la integridad referencial:** al eliminar un rol",
    rolesLogic, 'csharp');

content = replaceCodeBlock(content,
    "### 📄 `SupervisorPage.xaml` (Pantalla Restringida)",
    "### ⚙️ `SupervisorPage.xaml.cs` (Lógica Restringida)",
    getFile('Views\\\\SupervisorPage.xaml'), 'xml');

content = replaceCodeBlock(content,
    "### ⚙️ `SupervisorPage.xaml.cs` (Lógica Restringida)",
    "> 💡 **Idea de extensión:** este espacio (\"Ventana: Reportes y supervisión\")",
    getFile('Views\\\\SupervisorPage.xaml.cs'), 'csharp');

content = replaceCodeBlock(content,
    "### 📄 `VendedorPage.xaml` (Pantalla Restringida)",
    "### ⚙️ `VendedorPage.xaml.cs` (Lógica Restringida)",
    getFile('Views\\\\VendedorPage.xaml'), 'xml');

content = replaceCodeBlock(content,
    "### ⚙️ `VendedorPage.xaml.cs` (Lógica Restringida)",
    "> 💡 **Idea de extensión:** el \"Módulo de ventas\" es el lugar",
    getFile('Views\\\\VendedorPage.xaml.cs'), 'csharp');

content = content.replace(
    'Abre `AppShell.xaml` y reemplaza su contenido por este.',
    'Abre `AppShell.xaml` y reemplaza su contenido por este (nota el uso de `xmlns:views`).'
);
content = content.replace(
    'Crea la clase estática `Config.cs` en la raíz del proyecto.',
    'Crea una carpeta llamada `Controllers` en la raíz del proyecto y dentro de ella crea la clase estática `Config.cs`.'
);
content = content.replace(
    '1. Clic derecho en el proyecto → **Add** → **Class...**\n2. Nómbrala `Config.cs`.',
    '1. Crea la carpeta `Controllers`.\n2. Clic derecho en `Controllers` → **Add** → **Class...**\n3. Nómbrala `Config.cs`.'
);
content = content.replace(
    '4. Visual Studio generará automáticamente `AdminPage.xaml` y su code-behind `AdminPage.xaml.cs`.',
    '4. Visual Studio generará automáticamente `AdminPage.xaml` y su code-behind `AdminPage.xaml.cs`. Mueve estos archivos a la carpeta `Views` (o créalos directamente allí) y crea el modelo `UsuarioItem.cs` en la carpeta `Models`.'
);

fs.writeFileSync(newReadmePath, content, 'utf8');
