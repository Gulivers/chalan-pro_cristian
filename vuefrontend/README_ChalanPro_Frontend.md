# Proyecto Chalan-Pro - Estructura Frontend Vue.js

Bienvenido al sistema **Chalan-Pro** – un sistema robusto y modular para gestionar contratos, comunidades, cuadrillas, cronogramas y notas de obra. Este archivo te guiará sobre cómo está organizado el **frontend** con Vue.js para que puedas entrar al código con confianza y estilo. 

---

## 📁 Estructura del Proyecto

```bash
src/
│
├── assets/                  # Estilos globales, imágenes, íconos
│   ├── css/                 # Archivos CSS base
│   ├── scss/                # Estilos personalizados (ej: Bootstrap override)
│   └── img/                 # Logos, íconos, gráficos
│
├── components/              # Componentes Vue reutilizables y modulares
│   ├── layout/              # Navbar, Footer, Sidebar
│   ├── contracts/           # Formulario, charts, modales de contrato
│   ├── houses/              # Vista de mapa, notas, etc.
│   └── schedule/            # Calendario, chats, discusiones
│
├── views/                   # Vistas principales del sistema (Login, Home, 
|    │   AboutView.vue
|    │   HomeView.vue
|    │   LoginView.vue
│    └── contract/            # Subvistas de contratos (WorkPrices, etc.)
|           ContractView.vue
|           WorkPricesView.vue
│
├── auth/                    # Servicios y lógica de autenticación (login, tokens)
├── router/                  # Configuración de rutas Vue Router
├── store/                   # Vuex (o Pinia) para manejo del estado global
├── utils/                   # Axios configs, helpers, funciones utilitarias
├── helpers/                 # Otros helpers y funciones personalizadas
├── mixins/                  # Mixins globales para reusar lógica (ej: authMixin)
├── types/                   # Archivos de definición de tipos (ej: vue-select.d.ts)
│
├── App.vue                 # Componente raíz
└── main.js                 # Punto de entrada principal de la app
```

---

## 🚀 Tips para Desarrolladores Nuevos

1. **Alias Everywhere!**
   - Usa alias como `@components`, `@views`, `@contracts`, etc.
   - ¡No más `../../../../../components/contracts` en tus imports!

   ```js
   import Navbar from '@components/layout/NavbarComponent.vue';
   import ContractForm from '@contracts/ContractFormComponent.vue';
   ```

2. **Separa por feature, no por tipo**
   - Cada módulo (como `contracts`, `schedule`) tiene sus propios componentes.
   - Más fácil escalar y mantener.

3. **Mantén tus imports limpios**
   - Prefiere PascalCase para componentes `.vue`
   - Usa helpers o mixins para lógica repetida

4. **No temas preguntar 🧠**
   - Si algo no está documentado, ¡pregunta o documenta tú mismo!

---

## 💬 Estándares del equipo

- Componentes `.vue`: PascalCase (ej: `ContractFormComponent.vue`)
- Vistas: `LoginView.vue`, `HomeView.vue`, etc.
- Estado global: por ahora se usa Vuex (en `store/`)

---

## 🧩 Recursos útiles

- [Documentación Vue.js](https://vuejs.org/guide/introduction.html)
- [Bootstrap 5.3 Docs](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Axios](https://axios-http.com/)

---

## 🛠️ En resumen
> Código limpio, modular
> ¡Aquí trabajamos con cariño y con buenas prácticas! 

¡Bienvenido a bordo de Chalan-Pro
