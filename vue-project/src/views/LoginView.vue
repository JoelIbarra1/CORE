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

    <div class="login-card" :class="{ 'expanded': mostrarPreguntas }">
      <!-- Header con logo y título -->
      <div class="header">
        <div class="logo">
          <div class="heart-logo">💕</div>
        </div>
        <h1 class="app-title">LoveMatch</h1>
        <p class="subtitle">{{ mostrarPreguntas ? 'Cuéntanos más sobre ti' : 'Encuentra tu alma gemela' }}</p>
      </div>

      <!-- Contenido del formulario -->
      <div class="form-container">
        <!-- Toggle buttons solo si no estamos en el modo preguntas -->
        <div v-if="!mostrarPreguntas" class="toggle-buttons">
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
        <div v-if="modoLogin && !mostrarPreguntas" class="form-section login-form">
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
        <div v-else-if="!modoLogin && !mostrarPreguntas" class="form-section register-form">
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
            <button @click="continueToQuestions" class="primary-btn">
              <span>Continuar</span>
              <div class="btn-glow"></div>
            </button>
          </div>
        </div>

        <!-- Sección de Preguntas -->
        <div v-else-if="mostrarPreguntas" class="form-section questions-form">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
          </div>
          
          <div class="question-counter">
            Pregunta {{ preguntaActualIndex + 1 }} de {{ preguntas.length }}
          </div>

          <div v-if="preguntaActual" class="question-card">
            <h3 class="question-title">{{ preguntaActual.texto }}</h3>
            <div class="question-category">{{ getCategoryLabel(preguntaActual.categoria) }}</div>
            
            <!-- Pregunta binaria (sí/no) -->
            <div v-if="preguntaActual.tipo === 'binaria'" class="binary-options">
              <label class="binary-option">
                <input 
                  type="radio" 
                  :name="`pregunta_${preguntaActual.id_pregunta}`"
                  value="si"
                  v-model="respuestas[preguntaActual.id_pregunta]"
                />
                <span class="binary-label">Sí</span>
              </label>
              <label class="binary-option">
                <input 
                  type="radio" 
                  :name="`pregunta_${preguntaActual.id_pregunta}`"
                  value="no"
                  v-model="respuestas[preguntaActual.id_pregunta]"
                />
                <span class="binary-label">No</span>
              </label>
            </div>

            <!-- Pregunta de escala (1-5) -->
            <div v-else-if="preguntaActual.tipo === 'escala'" class="scale-options">
              <div class="scale-labels">
                <span>Totalmente en desacuerdo</span>
                <span>Totalmente de acuerdo</span>
              </div>
              <div class="scale-inputs">
                <label v-for="n in 5" :key="n" class="scale-option">
                  <input 
                    type="radio" 
                    :name="`pregunta_${preguntaActual.id_pregunta}`"
                    :value="n.toString()"
                    v-model="respuestas[preguntaActual.id_pregunta]"
                  />
                  <span class="scale-number">{{ n }}</span>
                </label>
              </div>
            </div>

            <!-- Pregunta de texto libre -->
            <div v-else-if="preguntaActual.tipo === 'texto'" class="text-input">
              <textarea 
                v-model="respuestas[preguntaActual.id_pregunta]"
                :placeholder="'Escribe tu respuesta aquí...'"
                class="modern-textarea"
                rows="4"
              ></textarea>
            </div>

            <!-- Pregunta múltiple - VERSIÓN MEJORADA -->
            <div v-else-if="preguntaActual.tipo === 'multiple'" class="multiple-options">
              <div class="multiple-note">Selecciona tus géneros musicales favoritos</div>
              
              <div class="checkbox-grid">
                <label 
                  v-for="genero in generosDisponibles" 
                  :key="genero" 
                  class="checkbox-item"
                >
                  <input 
                    type="checkbox" 
                    :value="genero"
                    @change="actualizarGenerosSeleccionados"
                    :checked="generosSeleccionados.includes(genero)"
                    class="checkbox-input"
                  />
                  <span class="checkbox-label">{{ genero }}</span>
                </label>
              </div>
              
              <!-- Campo oculto que contiene los géneros separados por coma -->
              <input 
                type="hidden"
                v-model="respuestas[preguntaActual.id_pregunta]"
              />
              
              <!-- Mostrar géneros seleccionados -->
              <div v-if="generosSeleccionados.length > 0" class="selected-genres">
                <strong>Géneros seleccionados:</strong> {{ generosSeleccionados.join(', ') }}
              </div>
            </div>
          </div>

          <div class="navigation-buttons">
            <button 
              v-if="preguntaActualIndex > 0" 
              @click="preguntaAnterior" 
              class="nav-btn secondary-btn"
            >
              ← Anterior
            </button>
            
            <button 
              v-if="preguntaActualIndex < preguntas.length - 1" 
              @click="preguntaSiguiente" 
              class="nav-btn primary-btn"
              :disabled="!respuestas[preguntaActual.id_pregunta]"
            >
              Siguiente →
            </button>
            
            <button 
              v-else 
              @click="completarRegistro" 
              class="nav-btn primary-btn"
              :disabled="!respuestas[preguntaActual.id_pregunta]"
            >
              Completar Registro ✨
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="error-message">
          <span class="error-icon">⚠️</span>
          {{ error }}
        </div>

        <!-- Loading -->
        <div v-if="loading" class="loading-message">
          <div class="spinner"></div>
          <span>{{ loadingMessage }}</span>
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
      mostrarPreguntas: false,
      preguntaActualIndex: 0,
      loading: false,
      loadingMessage: '',
      login: { email: '', password: '' },
      registro: {
        nombre: '',
        email: '',
        contraseña: '',
        fecha_nacimiento: '',
        genero: '',
        ubicacion: ''
      },
      preguntas: [],
      respuestas: {},
      error: '',
      usuarioRegistradoId: null,
      
      // Array de géneros musicales disponibles
      generosDisponibles: [
        'Rock',
        'Pop',
        'Jazz',
        'Reggaeton',
        'Salsa',
        'Merengue',
        'Bachata',
        'Cumbia',
        'Vallenato',
        'Hip Hop',
        'R&B',
        'Blues',
        'Country',
        'Folk',
        'Electrónica',
        'Reggae',
        'Punk',
        'Metal',
        'Clásica',
        'Bossa Nova',
        'Tango',
        'Ranchera',
        'Mariachi'
      ],
      
      // Array para géneros seleccionados
      generosSeleccionados: []
    };
  },
  computed: {
    preguntaActual() {
      return this.preguntas[this.preguntaActualIndex] || null;
    },
    progressPercentage() {
      if (this.preguntas.length === 0) return 0;
      return ((this.preguntaActualIndex + 1) / this.preguntas.length) * 100;
    }
  },
  methods: {
    async continueToQuestions() {
      // Validar datos del registro
      if (!this.registro.nombre || !this.registro.email || !this.registro.contraseña || 
          !this.registro.fecha_nacimiento || !this.registro.genero || !this.registro.ubicacion) {
        this.error = 'Por favor completa todos los campos';
        return;
      }

      this.loading = true;
      this.loadingMessage = 'Cargando preguntas...';
      this.error = '';

      try {
        // Cargar preguntas
        const response = await api.get('/preguntas');
        this.preguntas = response.data;
        
        if (this.preguntas.length === 0) {
          this.error = 'No hay preguntas disponibles. Contacta al administrador.';
          this.loading = false;
          return;
        }

        // Inicializar respuestas vacías
        this.respuestas = {};
        this.preguntas.forEach(pregunta => {
          this.respuestas[pregunta.id_pregunta] = '';
        });

        this.mostrarPreguntas = true;
        this.preguntaActualIndex = 0;
        
      } catch (err) {
        this.error = 'Error al cargar las preguntas. Inténtalo de nuevo.';
        console.error('Error cargando preguntas:', err);
      } finally {
        this.loading = false;
      }
    },

    preguntaSiguiente() {
      if (this.preguntaActualIndex < this.preguntas.length - 1) {
        this.preguntaActualIndex++;
      }
    },

    preguntaAnterior() {
      if (this.preguntaActualIndex > 0) {
        this.preguntaActualIndex--;
      }
    },

    // Método para actualizar géneros seleccionados
    actualizarGenerosSeleccionados(event) {
      const genero = event.target.value;
      
      if (event.target.checked) {
        // Agregar género si no está en la lista
        if (!this.generosSeleccionados.includes(genero)) {
          this.generosSeleccionados.push(genero);
        }
      } else {
        // Remover género de la lista
        const index = this.generosSeleccionados.indexOf(genero);
        if (index > -1) {
          this.generosSeleccionados.splice(index, 1);
        }
      }
      
      // Actualizar el campo de respuesta con géneros separados por coma
      this.respuestas[this.preguntaActual.id_pregunta] = this.generosSeleccionados.join(', ');
    },
    
    // Método para cargar géneros previamente seleccionados (si existen)
    cargarGenerosSeleccionados() {
      const respuestaActual = this.respuestas[this.preguntaActual.id_pregunta];
      if (respuestaActual) {
        this.generosSeleccionados = respuestaActual.split(', ').filter(g => g.trim() !== '');
      } else {
        this.generosSeleccionados = [];
      }
    },

    async completarRegistro() {
      this.loading = true;
      this.loadingMessage = 'Creando tu cuenta...';
      this.error = '';

      try {
        // Primero registrar el usuario
        const registroResponse = await api.post('/register', this.registro);
        this.usuarioRegistradoId = registroResponse.data.user_id;

        this.loadingMessage = 'Guardando tus respuestas...';

        // Luego hacer login para obtener el token
        const loginResponse = await api.post('/login', {
          email: this.registro.email,
          contraseña: this.registro.contraseña
        });

        const token = loginResponse.data.access_token;
        localStorage.setItem('token', token);
        localStorage.setItem('usuario_id', loginResponse.data.user_id);

        // Guardar todas las respuestas
        const respuestasValidas = Object.entries(this.respuestas)
          .filter(([preguntaId, respuesta]) => respuesta && respuesta.trim() !== '');

        let respuestasGuardadas = 0;
        for (const [preguntaId, respuesta] of respuestasValidas) {
          try {
            await api.post('/respuestas', {
              id_usuario: this.usuarioRegistradoId,
              id_pregunta: parseInt(preguntaId),
              respuesta: respuesta.toString().trim()
            });
            respuestasGuardadas++;
          } catch (respError) {
            console.error(`Error guardando respuesta para pregunta ${preguntaId}:`, respError);
          }
        }

        // Mostrar mensaje de éxito
        alert(`¡Registro completado exitosamente! Se guardaron ${respuestasGuardadas} respuestas.`);
        
        // Redirigir al usuario
        await new Promise(resolve => setTimeout(resolve, 500));
        this.$router.push('/usuario');

      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al completar el registro';
        console.error('Error en registro completo:', err);
      } finally {
        this.loading = false;
      }
    },

    getCategoryLabel(categoria) {
      const labels = {
        'valores': '💎 Valores',
        'intereses': '🎯 Intereses',
        'estilo_vida': '🌟 Estilo de Vida',
        'personalidad': '🧠 Personalidad'
      };
      return labels[categoria] || categoria;
    },

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
  },
  
  watch: {
    // Cargar géneros cuando cambie la pregunta actual
    preguntaActual: {
      handler() {
        if (this.preguntaActual && this.preguntaActual.tipo === 'multiple') {
          this.cargarGenerosSeleccionados();
        }
      },
      immediate: true
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
  transition: all 0.3s ease;
}

.login-card.expanded {
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
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
.modern-select,
.modern-textarea {
  flex: 1;
  padding: 16px 16px 16px 0;
  border: none;
  background: transparent;
  font-size: 16px;
  color: #333;
  outline: none;
  width: 100%;
}

.modern-textarea {
  resize: vertical;
  min-height: 80px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 16px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.modern-textarea:focus {
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.modern-input::placeholder,
.modern-textarea::placeholder {
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

/* Questions Styles */
.progress-bar {
  width: 100%;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  margin-bottom: 20px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.question-counter {
  text-align: center;
  color: #666;
  font-size: 14px;
  margin-bottom: 25px;
  font-weight: 500;
}

.question-card {
  background: #f8f9fa;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.question-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 0 0 15px 0;
  line-height: 1.4;
}

.question-category {
  display: inline-block;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 25px;
}

/* Binary Options */
.binary-options {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.binary-option {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 15px 25px;
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 16px;
  transition: all 0.3s ease;
  min-width: 120px;
  justify-content: center;
}

.binary-option:hover {
  border-color: #667eea;
  transform: translateY(-2px);
}

.binary-option input[type="radio"] {
  display: none;
}

.binary-option input[type="radio"]:checked + .binary-label {
  color: white;
}

.binary-option:has(input[type="radio"]:checked) {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: #667eea;
  color: white;
}

.binary-label {
  font-weight: 600;
  font-size: 16px;
}

/* Scale Options */
.scale-options {
  text-align: center;
}

.scale-labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.scale-inputs {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.scale-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding: 15px;
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 16px;
  transition: all 0.3s ease;
  flex: 1;
  min-width: 50px;
}

.scale-option:hover {
  border-color: #667eea;
  transform: translateY(-2px);
}

.scale-option input[type="radio"] {
  display: none;
}

.scale-option:has(input[type="radio"]:checked) {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: #667eea;
  color: white;
}

.scale-number {
  font-weight: 600;
  font-size: 18px;
  transition: color 0.3s ease;
}

/* Multiple Choice Options */
.multiple-options {
  text-align: left;
}

.multiple-note {
  background: #e3f2fd;
  color: #1976d2;
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  margin-bottom: 20px;
  font-weight: 500;
  border-left: 4px solid #1976d2;
}

.checkbox-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.checkbox-item {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 12px 16px;
  background: white;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.checkbox-item:hover {
  border-color: #667eea;
  transform: translateY(-1px);
}

.checkbox-item:has(input[type="checkbox"]:checked) {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-color: #667eea;
  color: white;
}

.checkbox-input {
  margin-right: 10px;
  width: 18px;
  height: 18px;
  accent-color: #667eea;
}

.checkbox-label {
  font-weight: 500;
  font-size: 14px;
}

.selected-genres {
  background: #f0f8ff;
  padding: 15px;
  border-radius: 12px;
  border-left: 4px solid #667eea;
  color: #333;
  font-size: 14px;
  margin-top: 15px;
}

/* Navigation Buttons */
.navigation-buttons {
  display: flex;
  gap: 15px;
  justify-content: space-between;
  margin-top: 30px;
}

.nav-btn {
  flex: 1;
  padding: 16px 32px;
  border: none;
  border-radius: 16px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.nav-btn:not(:disabled):hover {
  transform: translateY(-2px);
}

/* Button Groups */
.button-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 30px;
}

.primary-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 16px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
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
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.primary-btn:hover .btn-glow {
  left: 100%;
}

.secondary-btn {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.secondary-btn:hover {
  background: #667eea;
  color: white;
}

.admin-btn {
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.admin-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
}

/* Links */
.forgot-password {
  text-align: center;
  margin-top: 20px;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
  transition: color 0.3s ease;
}

.link:hover {
  color: #764ba2;
  text-decoration: underline;
}

/* Error and Loading Messages */
.error-message {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #ffebee;
  color: #c62828;
  padding: 15px;
  border-radius: 12px;
  margin-top: 20px;
  border-left: 4px solid #c62828;
  font-weight: 500;
}

.error-icon {
  font-size: 18px;
}

.loading-message {
  display: flex;
  align-items: center;
  gap: 15px;
  justify-content: center;
  padding: 20px;
  color: #667eea;
  font-weight: 500;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #e9ecef;
  border-top: 2px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
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
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 120' preserveAspectRatio='none'%3E%3Cpath d='M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z' fill='%23ffffff' fill-opacity='0.1'/%3E%3C/svg%3E") repeat-x;
  background-size: 1200px 100px;
  animation: wave 10s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% { transform: translateX(0); }
  50% { transform: translateX(-50px); }
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-container {
    padding: 10px;
  }
  
  .login-card {
    padding: 30px 20px;
    margin: 10px;
  }
  
  .login-card.expanded {
    max-width: 100%;
    margin: 0;
    border-radius: 0;
    min-height: 100vh;
  }
  
  .app-title {
    font-size: 28px;
  }
  
  .heart-logo {
    font-size: 40px;
  }
  
  .question-card {
    padding: 20px;
  }
  
  .binary-options {
    flex-direction: column;
    gap: 10px;
  }
  
  .binary-option {
    min-width: auto;
  }
  
  .scale-inputs {
    gap: 5px;
  }
  
  .scale-option {
    padding: 10px;
    min-width: 40px;
  }
  
  .checkbox-grid {
    grid-template-columns: 1fr;
  }
  
  .navigation-buttons {
    flex-direction: column;
  }
  
  .toggle-buttons {
    margin-bottom: 20px;
  }
  
  .scale-labels {
    font-size: 12px;
  }
  
  .question-title {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 20px 15px;
  }
  
  .app-title {
    font-size: 24px;
  }
  
  .heart-logo {
    font-size: 36px;
  }
  
  .question-card {
    padding: 15px;
  }
  
  .primary-btn, .nav-btn {
    padding: 14px 20px;
    font-size: 14px;
  }
  
  .scale-inputs {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .scale-option {
    flex: 0 0 calc(20% - 8px);
    min-width: 35px;
    padding: 8px;
  }
  
  .scale-number {
    font-size: 16px;
  }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  .heart {
    animation: none;
  }
  
  .wave {
    animation: none;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .login-card {
    border: 2px solid #000;
  }
  
  .input-wrapper {
    border: 2px solid #000;
  }
  
  .primary-btn {
    border: 2px solid #000;
  }
}

/* Focus styles for better accessibility */
.modern-input:focus,
.modern-select:focus,
.modern-textarea:focus,
.primary-btn:focus,
.secondary-btn:focus,
.admin-btn:focus,
.nav-btn:focus,
.toggle-btn:focus {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}

/* Print styles */
@media print {
  .login-container {
    background: white;
  }
  
  .background-hearts,
  .bottom-decoration {
    display: none;
  }
  
  .login-card {
    box-shadow: none;
    border: 1px solid #ccc;
  }
}
</style>