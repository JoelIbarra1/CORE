<template>
  <div class="admin-container">
    <!-- Header -->
    <div class="admin-header">
      <div class="header-content">
        <div class="brand">
          <div class="brand-icon">💕</div>
          <h1>Panel de Administración</h1>
        </div>
        <button @click="logout" class="logout-btn">
          <span class="logout-icon">🚪</span>
          Cerrar Sesión
        </button>
      </div>
    </div>

    <div class="admin-content">
      <!-- Gestión de Usuarios -->
      <section class="admin-section">
        <div class="section-header">
          <div class="section-title">
            <span class="section-icon">👥</span>
            <h2>Gestión de Usuarios</h2>
          </div>
        </div>

        <div class="form-card">
          <h3>Crear Nuevo Usuario</h3>
          <form @submit.prevent="crearUsuario" class="create-form">
            <div class="form-grid">
              <div class="form-group">
                <label>Nombre</label>
                <input v-model="nuevoUsuario.nombre" placeholder="Ingresa el nombre" required />
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="nuevoUsuario.email" placeholder="correo@ejemplo.com" required type="email" />
              </div>
              <div class="form-group">
                <label>Contraseña</label>
                <input v-model="nuevoUsuario.contraseña" placeholder="••••••••" required type="password" />
              </div>
              <div class="form-group">
                <label>Fecha de Nacimiento</label>
                <input v-model="nuevoUsuario.fecha_nacimiento" required type="date" />
              </div>
              <div class="form-group">
                <label>Género</label>
                <input v-model="nuevoUsuario.genero" placeholder="Género" />
              </div>
              <div class="form-group">
                <label>Ubicación</label>
                <input v-model="nuevoUsuario.ubicacion" placeholder="Ciudad, País" />
              </div>
            </div>
            <button type="submit" class="btn-primary">
              <span>✨</span>
              Crear Usuario
            </button>
          </form>
        </div>

        <div class="data-card">
          <h3>Lista de Usuarios</h3>
          <div class="users-grid">
            <div v-for="u in usuarios" :key="u.id_usuario" class="user-card">
              <div class="user-info">
                <div class="user-avatar">{{ u.nombre.charAt(0).toUpperCase() }}</div>
                <div class="user-details">
                  <h4>{{ u.nombre }}</h4>
                  <p>{{ u.email }}</p>
                  <span class="user-meta">📍 {{ u.ubicacion || 'Sin ubicación' }}</span>
                </div>
              </div>
              <div class="user-actions">
                <button @click="seleccionarUsuario(u)" class="btn-edit">
                  <span>✏️</span>
                </button>
                <button @click="eliminarUsuario(u.id_usuario)" class="btn-delete">
                  <span>🗑️</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="usuarioEditando" class="edit-modal">
          <div class="modal-content">
            <div class="modal-header">
              <h3>Editar Usuario</h3>
              <button @click="usuarioEditando = null" class="close-btn">✕</button>
            </div>
            <div class="form-grid">
              <div class="form-group">
                <label>Nombre</label>
                <input v-model="usuarioEditando.nombre" placeholder="Nombre" />
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="usuarioEditando.email" placeholder="Email" />
              </div>
              <div class="form-group">
                <label>Fecha de Nacimiento</label>
                <input v-model="usuarioEditando.fecha_nacimiento" type="date" />
              </div>
              <div class="form-group">
                <label>Género</label>
                <input v-model="usuarioEditando.genero" placeholder="Género" />
              </div>
              <div class="form-group">
                <label>Ubicación</label>
                <input v-model="usuarioEditando.ubicacion" placeholder="Ubicación" />
              </div>
            </div>
            <div class="modal-actions">
              <button @click="actualizarUsuario" class="btn-primary">
                <span>💾</span>
                Guardar Cambios
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Gestión de Respuestas -->
      <section class="admin-section">
        <div class="section-header">
          <div class="section-title">
            <span class="section-icon">💬</span>
            <h2>Gestión de Respuestas</h2>
          </div>
        </div>

        <div class="form-card">
          <h3>Crear Nueva Respuesta</h3>
          <form @submit.prevent="crearRespuesta" class="create-form">
            <div class="form-grid">
              <div class="form-group">
                <label>ID Usuario</label>
                <input v-model="nuevaRespuesta.id_usuario" placeholder="ID del usuario" required type="number" />
              </div>
              <div class="form-group">
                <label>ID Pregunta</label>
                <input v-model="nuevaRespuesta.id_pregunta" placeholder="ID de la pregunta" required type="number" />
              </div>
              <div class="form-group full-width">
                <label>Respuesta</label>
                <textarea v-model="nuevaRespuesta.respuesta" placeholder="Escribe la respuesta..." required></textarea>
              </div>
            </div>
            <button type="submit" class="btn-primary">
              <span>💭</span>
              Crear Respuesta
            </button>
          </form>
        </div>

        <div class="data-card">
          <h3>Lista de Respuestas</h3>
          <div class="responses-list">
            <div v-for="r in respuestas" :key="r.id_respuesta" class="response-card">
              <div class="response-info">
                <div class="response-meta">
                  <span class="user-id">👤 Usuario {{ r.id_usuario }}</span>
                  <span class="question-id">❓ Pregunta {{ r.id_pregunta }}</span>
                </div>
                <p class="response-text">"{{ r.respuesta }}"</p>
              </div>
              <div class="response-actions">
                <button @click="seleccionarRespuesta(r)" class="btn-edit">
                  <span>✏️</span>
                </button>
                <button @click="eliminarRespuesta(r.id_respuesta)" class="btn-delete">
                  <span>🗑️</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="respuestaEditando" class="edit-modal">
          <div class="modal-content">
            <div class="modal-header">
              <h3>Editar Respuesta</h3>
              <button @click="respuestaEditando = null" class="close-btn">✕</button>
            </div>
            <div class="form-group">
              <label>Respuesta</label>
              <textarea v-model="respuestaEditando.respuesta" placeholder="Respuesta"></textarea>
            </div>
            <div class="modal-actions">
              <button @click="actualizarRespuesta" class="btn-primary">
                <span>💾</span>
                Guardar Cambios
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Compatibilidades -->
      <section class="admin-section">
        <div class="section-header">
          <div class="section-title">
            <span class="section-icon">💖</span>
            <h2>Análisis de Compatibilidades</h2>
          </div>
        </div>

        <div class="form-card">
          <h3>Filtros de Compatibilidad</h3>
          <div class="compatibility-controls">
            <div class="form-group">
              <label>ID Usuario</label>
              <input v-model="usuarioIdFiltro" type="number" placeholder="Filtrar por usuario" />
            </div>
            <div class="form-group">
              <label>Límite de Resultados</label>
              <input v-model.number="limiteCompat" type="number" placeholder="100" />
            </div>
            <div class="button-group">
              <button @click="getCompatibilidades" class="btn-secondary">
                <span>🔍</span>
                Ver Compatibilidades
              </button>
              <button @click="calcularCompatibilidades" class="btn-primary">
                <span>⚡</span>
                Calcular Masivo
              </button>
            </div>
          </div>
        </div>

        <div class="data-card" v-if="compatibilidades.length > 0">
          <h3>Resultados de Compatibilidad</h3>
          <div class="compatibility-grid">
            <div v-for="c in compatibilidades" :key="c.id_resultado" class="compatibility-card">
              <div class="compatibility-info">
                <div class="users-match">
                  <span class="user-origin">👤 {{ c.id_usuario_origen }}</span>
                  <span class="match-icon">💕</span>
                  <span class="user-compared">👤 {{ c.id_usuario_comparado }}</span>
                </div>
                <div class="compatibility-score">
                  <div class="score-circle" :style="{ background: getScoreColor(c.porcentaje_compatibilidad) }">
                    <span>{{ c.porcentaje_compatibilidad }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Mensajes de Estado -->
      <div class="notifications">
        <div v-if="mensaje" class="notification success">
          <span class="notification-icon">✅</span>
          {{ mensaje }}
        </div>
        <div v-if="error" class="notification error">
          <span class="notification-icon">❌</span>
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../axios';

export default {
  data() {
    return {
      usuarios: [],
      usuarioEditando: null,
      nuevoUsuario: {
        nombre: '',
        email: '',
        contraseña: '',
        fecha_nacimiento: '',
        genero: '',
        ubicacion: ''
      },
      respuestas: [],
      nuevaRespuesta: {
        id_usuario: '',
        id_pregunta: '',
        respuesta: ''
      },
      respuestaEditando: null,
      compatibilidades: [],
      usuarioIdFiltro: '',
      limiteCompat: 100,
      mensaje: '',
      error: ''
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/');
    },
    clearMensajes() {
      this.mensaje = '';
      this.error = '';
    },
    getScoreColor(score) {
      if (score >= 80) return 'linear-gradient(135deg, #ff6b6b, #ff8e8e)';
      if (score >= 60) return 'linear-gradient(135deg, #ffa726, #ffcc80)';
      if (score >= 40) return 'linear-gradient(135deg, #42a5f5, #90caf9)';
      return 'linear-gradient(135deg, #78909c, #b0bec5)';
    },

    // Usuarios
    async getUsuarios() {
      this.clearMensajes();
      try {
        const res = await api.get('/admin/usuarios');
        this.usuarios = res.data;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al obtener usuarios';
      }
    },
    async crearUsuario() {
      this.clearMensajes();
      try {
        await api.post('/admin/usuarios', this.nuevoUsuario);
        this.mensaje = 'Usuario creado exitosamente';
        this.nuevoUsuario = {
          nombre: '',
          email: '',
          contraseña: '',
          fecha_nacimiento: '',
          genero: '',
          ubicacion: ''
        };
        this.getUsuarios();
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al crear usuario';
      }
    },
    seleccionarUsuario(usuario) {
      this.usuarioEditando = { ...usuario };
    },
    async actualizarUsuario() {
      this.clearMensajes();
      try {
        await api.put(`/admin/usuarios/${this.usuarioEditando.id_usuario}`, this.usuarioEditando);
        this.mensaje = 'Usuario actualizado exitosamente';
        this.usuarioEditando = null;
        this.getUsuarios();
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al actualizar usuario';
      }
    },
    async eliminarUsuario(id) {
      if (confirm('¿Estás seguro de eliminar este usuario?')) {
        this.clearMensajes();
        try {
          await api.delete(`/admin/usuarios/${id}`);
          this.mensaje = 'Usuario eliminado exitosamente';
          this.getUsuarios();
        } catch (err) {
          this.error = err.response?.data?.detail || 'Error al eliminar usuario';
        }
      }
    },

    // Respuestas
    async getRespuestas() {
      this.clearMensajes();
      try {
        const res = await api.get('/admin/respuestas');
        this.respuestas = res.data;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al obtener respuestas';
      }
    },
    async crearRespuesta() {
      this.clearMensajes();
      try {
        await api.post('/admin/respuestas', this.nuevaRespuesta);
        this.mensaje = 'Respuesta creada exitosamente';
        this.nuevaRespuesta = {
          id_usuario: '',
          id_pregunta: '',
          respuesta: ''
        };
        this.getRespuestas();
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al crear respuesta';
      }
    },
    seleccionarRespuesta(r) {
      this.respuestaEditando = { ...r };
    },
    async actualizarRespuesta() {
      this.clearMensajes();
      try {
        await api.put(`/admin/respuestas/${this.respuestaEditando.id_respuesta}`, {
          respuesta: this.respuestaEditando.respuesta
        });
        this.mensaje = 'Respuesta actualizada exitosamente';
        this.respuestaEditando = null;
        this.getRespuestas();
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al actualizar respuesta';
      }
    },
    async eliminarRespuesta(id) {
      if (confirm('¿Estás seguro de eliminar esta respuesta?')) {
        this.clearMensajes();
        try {
          await api.delete(`/admin/respuestas/${id}`);
          this.mensaje = 'Respuesta eliminada exitosamente';
          this.getRespuestas();
        } catch (err) {
          this.error = err.response?.data?.detail || 'Error al eliminar respuesta';
        }
      }
    },

    // Compatibilidad
    async getCompatibilidades() {
      this.clearMensajes();
      try {
        const params = {};
        if (this.usuarioIdFiltro) params.usuario_id = this.usuarioIdFiltro;
        if (this.limiteCompat) params.limite = this.limiteCompat;

        const res = await api.get('/admin/compatibilidades', { params });
        this.compatibilidades = res.data;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al obtener compatibilidades';
      }
    },
    async calcularCompatibilidades() {
      this.clearMensajes();
      try {
        const res = await api.post('/admin/calcular-compatibilidad-masiva');
        this.mensaje = `Compatibilidades procesadas: ${res.data.resultados_procesados}`;
      } catch (err) {
        this.error = err.response?.data?.detail || 'Error al calcular compatibilidad';
      }
    }
  },
  mounted() {
    this.getUsuarios();
    this.getRespuestas();
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.admin-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

/* Header */
.admin-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.brand-icon {
  font-size: 2rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.brand h1 {
  color: white;
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

/* Content */
.admin-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.admin-section {
  margin-bottom: 3rem;
}

.section-header {
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.section-icon {
  font-size: 2rem;
}

.section-title h2 {
  color: white;
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
}

/* Cards */
.form-card, .data-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.form-card h3, .data-card h3 {
  margin: 0 0 1.5rem 0;
  color: #333;
  font-size: 1.3rem;
  font-weight: 600;
}

/* Forms */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: 600;
  color: #555;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-group input, .form-group textarea {
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.form-group input:focus, .form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

/* Buttons */
.btn-primary, .btn-secondary, .btn-edit, .btn-delete {
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 1rem 2rem;
  font-size: 1rem;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
  background: linear-gradient(135deg, #42a5f5, #478ed1);
  color: white;
  padding: 1rem 2rem;
  font-size: 1rem;
}

.btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(66, 165, 245, 0.3);
}

.btn-edit {
  background: linear-gradient(135deg, #ffa726, #ffcc80);
  color: white;
  padding: 0.5rem;
  width: 40px;
  height: 40px;
  border-radius: 10px;
}

.btn-edit:hover {
  transform: scale(1.1);
}

.btn-delete {
  background: linear-gradient(135deg, #ef5350, #ff8a80);
  color: white;
  padding: 0.5rem;
  width: 40px;
  height: 40px;
  border-radius: 10px;
}

.btn-delete:hover {
  transform: scale(1.1);
}

/* User Grid */
.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.user-card {
  background: linear-gradient(135deg, #f8f9ff, #ffffff);
  border-radius: 15px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 2px solid #f0f0f0;
  transition: all 0.3s ease;
}

.user-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
}

.user-details h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
  font-size: 1.1rem;
}

.user-details p {
  margin: 0 0 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.user-meta {
  font-size: 0.8rem;
  color: #999;
}

.user-actions {
  display: flex;
  gap: 0.5rem;
}

/* Responses */
.responses-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.response-card {
  background: linear-gradient(135deg, #f8f9ff, #ffffff);
  border-radius: 15px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border: 2px solid #f0f0f0;
  transition: all 0.3s ease;
}

.response-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
}

.response-info {
  flex: 1;
}

.response-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.user-id, .question-id {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.response-text {
  color: #333;
  margin: 0;
  font-style: italic;
  line-height: 1.5;
}

.response-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: 1rem;
}

/* Compatibility */
.compatibility-controls {
  display: grid;
  grid-template-columns: 1fr 1fr 2fr;
  gap: 1.5rem;
  align-items: end;
}

.button-group {
  display: flex;
  gap: 1rem;
}

.compatibility-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.compatibility-card {
  background: linear-gradient(135deg, #f8f9ff, #ffffff);
  border-radius: 15px;
  padding: 1.5rem;
  border: 2px solid #f0f0f0;
  transition: all 0.3s ease;
}

.compatibility-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
}

.users-match {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.user-origin, .user-compared {
  background: #e8eaf6;
  color: #3f51b5;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.match-icon {
  font-size: 1.5rem;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.compatibility-score {
  display: flex;
  justify-content: center;
}

.score-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.1rem;
}

/* Modal */
.edit-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f0f0f0;
}

.modal-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.4rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0.5rem;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #f5f5f5;
  color: #333;
  transform: scale(1.1);
}

.modal-actions {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

/* Notifications */
.notifications {
  position: fixed;
  top: 100px;
  right: 2rem;
  z-index: 1100;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.notification {
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 300px;
  animation: slideIn 0.3s ease-out;
  border-left: 4px solid;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.notification.success {
  border-left-color: #4caf50;
  background: linear-gradient(135deg, #e8f5e8, #ffffff);
}

.notification.error {
  border-left-color: #f44336;
  background: linear-gradient(135deg, #ffeaea, #ffffff);
}

.notification-icon {
  font-size: 1.2rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .admin-content {
    padding: 1rem;
  }
  
  .header-content {
    padding: 0 1rem;
    flex-direction: column;
    gap: 1rem;
  }
  
  .brand h1 {
    font-size: 1.5rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .compatibility-controls {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .button-group {
    flex-direction: column;
  }
  
  .users-grid {
    grid-template-columns: 1fr;
  }
  
  .compatibility-grid {
    grid-template-columns: 1fr;
  }
  
  .user-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .user-actions {
    align-self: flex-end;
  }
  
  .response-card {
    flex-direction: column;
    gap: 1rem;
  }
  
  .response-actions {
    margin-left: 0;
    align-self: flex-end;
  }
  
  .users-match {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .modal-content {
    width: 95%;
    padding: 1.5rem;
  }
  
  .notifications {
    right: 1rem;
    left: 1rem;
  }
  
  .notification {
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .section-title {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .section-title h2 {
    font-size: 1.5rem;
  }
  
  .form-card, .data-card {
    padding: 1.5rem;
  }
  
  .user-card, .response-card, .compatibility-card {
    padding: 1rem;
  }
  
  .modal-content {
    padding: 1rem;
  }
  
  .btn-primary, .btn-secondary {
    padding: 0.875rem 1.5rem;
    font-size: 0.95rem;
  }
}

/* Loading States */
.loading {
  opacity: 0.6;
  pointer-events: none;
}

.loading::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  margin: -10px 0 0 -10px;
  border: 2px solid #667eea;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Accessibility Improvements */
.btn-primary:focus,
.btn-secondary:focus,
.btn-edit:focus,
.btn-delete:focus,
.logout-btn:focus {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

/* Dark mode support (optional) */
@media (prefers-color-scheme: dark) {
  .form-card, .data-card {
    background: rgba(30, 30, 30, 0.95);
    color: #fff;
  }
  
  .form-card h3, .data-card h3 {
    color: #fff;
  }
  
  .form-group label {
    color: #ccc;
  }
  
  .form-group input,
  .form-group textarea {
    background: #2a2a2a;
    border-color: #444;
    color: #fff;
  }
  
  .user-card,
  .response-card,
  .compatibility-card {
    background: linear-gradient(135deg, #2a2a2a, #1a1a1a);
    border-color: #444;
  }
  
  .user-details h4 {
    color: #fff;
  }
  
  .user-details p {
    color: #ccc;
  }
  
  .response-text {
    color: #ccc;
  }
}

/* Smooth transitions for all interactive elements */
* {
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>