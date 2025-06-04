<template>
  <div class="login-container">
    <!-- Fondo animado con partículas de corazones -->
    <div class="background-hearts">
      <div class="heart" v-for="n in 15" :key="n" :style="{ 
        left: Math.random() * 100 + '%', 
        animationDelay: Math.random() * 3 + 's',
        animationDuration: (3 + Math.random() * 2) + 's'
      }">♥</div>
    </div>

    <div class="login-card">
      <!-- Header con logo y título -->
      <div class="header">
        <div class="logo">
          <div class="heart-logo">💕</div>
        </div>
        <h1 class="app-title">LoveMatch</h1>
        <p class="subtitle">Encuentra tu alma gemela</p>
      </div>

      <!-- Contenido del formulario -->
      <div class="form-container">
        <div class="toggle-buttons">
          <button 
            :class="['toggle-btn', { active: modoLogin }]"
            @click="modoLogin = true"
          >
            Iniciar Sesión
          </button>
          <button 
            :class="['toggle-btn', { active: !modoLogin }]"
            @click="modoLogin = false"
          >
            Registro
          </button>
        </div>

        <!-- Formulario de Login -->
        <div v-if="modoLogin" class="form-section login-form">
          <div class="input-group">
            <div class="input-wrapper">
              <span class="input-icon">📧</span>
              <input 
                v-model="login.email" 
                type="email"
                placeholder="Tu email"
                class="modern-input"
              />
            </div>
          </div>

          <div class="input-group">
            <div class="input-wrapper">
              <span class="input-icon">🔒</span>
              <input 
                v-model="login.password" 
                type="password"
                placeholder="Tu contraseña"
                class="modern-input"
              />
            </div>
          </div>

          <div class="button-group">
            <button @click="loginUser" class="primary-btn">
              <span>Iniciar Sesión</span>
              <div class="btn-glow"></div>
            </button>
            
            <button @click="loginAdmin" class="admin-btn">
              <span>👑 Admin</span>
            </button>
          </div>

          <div class="forgot-password">
            <a href="#" class="link">¿Olvidaste tu contraseña?</a>
          </div>
        </div>

        <!-- Formulario de Registro -->
        <div v-else class="form-section register-form">
          <div class="input-group">
            <div class="input-wrapper">
              <span class="input-icon">👤</span>
              <input 
                v-model="registro.nombre" 
                placeholder="Tu nombre completo"
                class="modern-input"
              />
            </div>
          </div>

          <div class="input-group">
            <div class="input-wrapper">
              <span class="input-icon">📧</span>
              <input 
                v-model="registro.email" 
                type="email"
                placeholder="Tu email"
                class="modern-input"
              />
            </div>
          </div>

          <div class="input-group">
            <div class="input-wrapper">
              <span class="input-icon">🔒</span>
              <input 
                v-model="registro.contraseña" 
                type="password"
                placeholder="Crea una contraseña"
                class="modern-input"
              />
            </div>
          </div>

          <div class="input-group">
            <div class="input-wrapper">
              <span class="input-icon">🎂</span>
              <input 
                v-model="registro.fecha_nacimiento" 
                type="date"
                class="modern-input date-input"
              />
            </div>
          </div>

          <div class="input-group">
            <div class="input-wrapper">
              <span class="input-icon">⚧</span>
              <select v-model="registro.genero" class="modern-select">
                <option value="" disabled>Selecciona tu género</option>
                <option value="masculino">Masculino</option>
                <option value="femenino">Femenino</option>
                <option value="no_binario">No binario</option>
                <option value="prefiero_no_decir">Prefiero no decir</option>
              </select>
            </div>
          </div>

          <div class="input-group">
            <div class="input-wrapper">
              <span class="input-icon">📍</span>
              <input 
                v-model="registro.ubicacion" 
                placeholder="Tu ubicación"
                class="modern-input"
              />
            </div>
          </div>

          <div class="button-group">
            <button @click="registerUser" class="primary-btn">
              <span>Crear Cuenta</span>
              <div class="btn-glow"></div>
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="error-message">
          <span class="error-icon">⚠️</span>
          {{ error }}
        </div>
      </div>
    </div>

    <!-- Decoración inferior -->
    <div class="bottom-decoration">
      <div class="wave"></div>
    </div>
  </div>
</template>

<script>
import api from '../axios';

export default {
  data() {
    return {
      modoLogin: true,
      login: { email: '', password: '' },
      registro: {
        nombre: '',
        email: '',
        contraseña: '',
        fecha_nacimiento: '',
        genero: '',
        ubicacion: ''
      },
      error: ''
    };
  },
  methods: {
    async registerUser() {
      try {
        await api.post('/register', this.registro);
        alert('¡Registro exitoso! Ahora puedes iniciar sesión');
        this.modoLogin = true;
        this.error = '';
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al registrar';
      }
    },
    async loginUser() {
      try {
        const res = await api.post('/login', {
          email: this.login.email,
          contraseña: this.login.password
        });

        localStorage.setItem('token', res.data.access_token);
        localStorage.setItem('usuario_id', res.data.user_id);

        console.log("Usuario ID guardado:", localStorage.getItem('usuario_id'));

        await new Promise(resolve => setTimeout(resolve, 100));

        this.$router.push('/usuario');
      } catch (err) {
        this.error = err.response?.data?.detail || 'Credenciales incorrectas';
      }
    },
    async loginAdmin() {
      try {
        const res = await api.post('/admin/login', {
          email: this.login.email,
          contraseña: this.login.password
        });
        localStorage.setItem('token', res.data.access_token);
        this.$router.push('/admin');
      } catch (err) {
        this.error = err.response?.data?.detail || 'Acceso de admin denegado';
      }
    }
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

/* Fondo animado con corazones */
.background-hearts {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.heart {
  position: absolute;
  color: rgba(255, 255, 255, 0.1);
  font-size: 20px;
  animation: floating 4s ease-in-out infinite;
}

@keyframes floating {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) rotate(360deg);
    opacity: 0;
  }
}

/* Tarjeta principal */
.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.2);
  width: 100%;
  max-width: 450px;
  animation: slideUp 0.6s ease-out;
  position: relative;
  z-index: 10;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Header */
.header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  margin-bottom: 20px;
}

.heart-logo {
  font-size: 48px;
  background: linear-gradient(45deg, #ff6b6b, #ff8e8e, #ffa8a8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.app-title {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  letter-spacing: -1px;
}

.subtitle {
  color: #666;
  font-size: 16px;
  margin: 8px 0 0 0;
  font-weight: 300;
}

/* Toggle Buttons */
.toggle-buttons {
  display: flex;
  background: #f8f9fa;
  border-radius: 16px;
  padding: 4px;
  margin-bottom: 30px;
  position: relative;
}

.toggle-btn {
  flex: 1;
  padding: 12px 20px;
  border: none;
  background: transparent;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #666;
  position: relative;
  z-index: 2;
}

.toggle-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* Form Sections */
.form-section {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}

/* Input Groups */
.input-group {
  margin-bottom: 20px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: #f8f9fa;
  border-radius: 16px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  overflow: hidden;
}

.input-wrapper:focus-within {
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.input-icon {
  padding: 0 16px;
  font-size: 18px;
  color: #999;
  transition: color 0.3s ease;
}

.input-wrapper:focus-within .input-icon {
  color: #667eea;
}

.modern-input,
.modern-select {
  flex: 1;
  padding: 16px 16px 16px 0;
  border: none;
  background: transparent;
  font-size: 16px;
  color: #333;
  outline: none;
}

.modern-input::placeholder {
  color: #999;
  font-weight: 300;
}

.modern-select {
  cursor: pointer;
  color: #333;
}

.modern-select option {
  padding: 10px;
  background: white;
}

.date-input {
  color: #666;
}

/* Buttons */
.button-group {
  margin: 30px 0 20px 0;
}

.primary-btn {
  width: 100%;
  padding: 16px;
  border: none;
  border-radius: 16px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  margin-bottom: 12px;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.primary-btn:active {
  transform: translateY(0);
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.primary-btn:hover .btn-glow {
  left: 100%;
}

.admin-btn {
  width: 100%;
  padding: 12px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  background: white;
  color: #666;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.admin-btn:hover {
  border-color: #ffd700;
  color: #f39c12;
  transform: translateY(-1px);
}

/* Links */
.forgot-password {
  text-align: center;
  margin-top: 20px;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.3s ease;
}

.link:hover {
  color: #764ba2;
  text-decoration: underline;
}

/* Error Message */
.error-message {
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
  color: white;
  padding: 12px 16px;
  border-radius: 12px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 500;
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.error-icon {
  font-size: 16px;
}

/* Bottom Decoration */
.bottom-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  pointer-events: none;
}

.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' opacity='.25' fill='%23FFFFFF'%3E%3C/path%3E%3Cpath d='M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z' opacity='.5' fill='%23FFFFFF'%3E%3C/path%3E%3Cpath d='M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z' fill='%23FFFFFF'%3E%3C/path%3E%3C/svg%3E") no-repeat;
  background-size: cover;
  opacity: 0.3;
}

/* Responsive */
@media (max-width: 768px) {
  .login-card {
    padding: 30px 20px;
    margin: 10px;
    border-radius: 20px;
  }
  
  .app-title {
    font-size: 28px;
  }
  
  .input-wrapper {
    border-radius: 12px;
  }
  
  .primary-btn {
    border-radius: 12px;
  }
}

@media (max-width: 480px) {
  .login-container {
    padding: 10px;
  }
  
  .login-card {
    padding: 20px 15px;
  }
  
  .heart-logo {
    font-size: 40px;
  }
  
  .app-title {
    font-size: 24px;
  }
}
</style>