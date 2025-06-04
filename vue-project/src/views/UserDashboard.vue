<template>
  <div class="dashboard">
    <!-- Background animated elements -->
    <div class="bg-decoration">
      <div class="floating-heart heart-1">💕</div>
      <div class="floating-heart heart-2">💖</div>
      <div class="floating-heart heart-3">✨</div>
      <div class="floating-heart heart-4">💫</div>
    </div>

    <div class="header">
      <div class="header-content">
        <div class="title-section">
          <h1 class="main-title">
            <span class="heart-icon">💝</span>
            Mis Mejores Matches
          </h1>
          <p class="subtitle">Descubre conexiones especiales</p>
        </div>
        <button @click="logout" class="logout-btn">
          <span class="logout-icon">👋</span>
          Cerrar Sesión
        </button>
      </div>
    </div>

    <!-- Filtros mejorados -->
    <section class="filters">
      <div class="filter-header">
        <h3>
          <span class="filter-icon">🔍</span>
          Filtrar por género
        </h3>
      </div>
      <div class="filter-options">
        <label class="filter-option" :class="{ active: filtroGenero === '' }">
          <input 
            type="radio" 
            value="" 
            v-model="filtroGenero" 
            @change="aplicarFiltro"
          />
          <span class="radio-custom"></span>
          <span class="filter-text">Todos</span>
        </label>
        <label class="filter-option" :class="{ active: filtroGenero === 'masculino' }">
          <input 
            type="radio" 
            value="masculino" 
            v-model="filtroGenero" 
            @change="aplicarFiltro"
          />
          <span class="radio-custom"></span>
          <span class="filter-text">Masculino</span>
        </label>
        <label class="filter-option" :class="{ active: filtroGenero === 'femenino' }">
          <input 
            type="radio" 
            value="femenino" 
            v-model="filtroGenero" 
            @change="aplicarFiltro"
          />
          <span class="radio-custom"></span>
          <span class="filter-text">Femenino</span>
        </label>
        <label class="filter-option" :class="{ active: filtroGenero === 'no_binario' }">
          <input 
            type="radio" 
            value="no_binario" 
            v-model="filtroGenero" 
            @change="aplicarFiltro"
          />
          <span class="radio-custom"></span>
          <span class="filter-text">No binario</span>
        </label>
        <label class="filter-option" :class="{ active: filtroGenero === 'prefiero_no_decir' }">
          <input 
            type="radio" 
            value="prefiero_no_decir" 
            v-model="filtroGenero" 
            @change="aplicarFiltro"
          />
          <span class="radio-custom"></span>
          <span class="filter-text">Prefiero no decir</span>
        </label>
      </div>
    </section>

    <!-- Sección de matches mejorada -->
    <section class="matches-section">
      <div class="section-header">
        <h3>
          <span class="matches-icon">🌟</span>
          Mejores Matches 
          <span class="count">({{ matchesFiltrados.length }} resultados)</span>
        </h3>
      </div>
      
      <div v-if="loading" class="loading">
        <div class="loading-spinner"></div>
        <p>Buscando tus matches perfectos...</p>
      </div>
      
      <div v-else-if="matchesFiltrados.length === 0" class="no-matches">
        <div class="no-matches-icon">💔</div>
        <h4>No hay matches aún</h4>
        <p v-if="filtroGenero">No encontramos matches para el género seleccionado.</p>
        <p v-else>¡Pronto encontrarás conexiones increíbles!</p>
      </div>
      
      <div v-else class="matches-grid">
        <div 
          v-for="(m, index) in matchesFiltrados" 
          :key="m.usuario_comparado.id_usuario"
          class="match-card"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="match-glow"></div>
          
          <div class="match-header">
            <div class="user-info">
              <div class="avatar">
                {{ m.usuario_comparado.nombre.charAt(0).toUpperCase() }}
              </div>
              <h4>{{ m.usuario_comparado.nombre }}</h4>
            </div>
            <div class="compatibility-badge" :class="getCompatibilityClass(m.porcentaje_compatibilidad)">
              <div class="percentage">{{ m.porcentaje_compatibilidad.toFixed(1) }}%</div>
              <div class="compatibility-text">Match</div>
            </div>
          </div>
          
          <div class="match-info">
            <div class="info-item">
              <span class="label">
                <span class="info-icon">📍</span>
                Ubicación
              </span>
              <span class="value">{{ m.usuario_comparado.ubicacion || 'No disponible' }}</span>
            </div>
            
            <div class="info-item">
              <span class="label">
                <span class="info-icon">👤</span>
                Género
              </span>
              <span class="value">{{ formatGenero(m.usuario_comparado.genero) }}</span>
            </div>
            
            <div class="info-item">
              <span class="label">
                <span class="info-icon">📅</span>
                Calculado
              </span>
              <span class="value">{{ formatFecha(m.fecha_calculo) }}</span>
            </div>
          </div>

          <div class="match-actions">
            <button class="action-btn primary">
              <span class="btn-icon">💌</span>
              Enviar Mensaje
            </button>
            <button class="action-btn secondary">
              <span class="btn-icon">👀</span>
              Ver Perfil
            </button>
          </div>
        </div>
      </div>
    </section>

    <div v-if="error" class="error">
      <span class="error-icon">⚠️</span>
      {{ error }}
    </div>
  </div>
</template>

<script>
import api from '../axios';

export default {
  data() {
    return {
      mejoresMatches: [],
      filtroGenero: '',
      loading: false,
      error: ''
    };
  },
  computed: {
    matchesFiltrados() {
      if (!this.filtroGenero) {
        return this.mejoresMatches;
      }
      return this.mejoresMatches.filter(match => 
        match.usuario_comparado.genero === this.filtroGenero
      );
    }
  },
  mounted() {
    console.log("usuario_id en mounted:", localStorage.getItem('usuario_id'));
    this.getMejoresMatches();
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('usuario_id');
      this.$router.push('/');
    },
    
    async getMejoresMatches() {
      this.loading = true;
      try {
        let usuario_id = localStorage.getItem('usuario_id');

        if (!usuario_id) {
          console.warn("usuario_id aún no está definido, reintentando en 100ms...");
          await new Promise(resolve => setTimeout(resolve, 100));
          usuario_id = localStorage.getItem('usuario_id');
        }

        if (!usuario_id) {
          throw new Error("No se encontró usuario_id en localStorage después del reintento");
        }

        const limite = 20;
        console.log("Solicitando mejores matches para usuario:", usuario_id, "con límite:", limite);

        const res = await api.get('/mejores-matches', {
          params: { usuario_id, limite }
        });

        this.mejoresMatches = res.data;
      } catch (err) {
        console.error(err);
        this.error = err.response?.data?.detail || err.message || 'Error al cargar mejores matches';
      } finally {
        this.loading = false;
      }
    },
    
    aplicarFiltro() {
      console.log("Filtro aplicado:", this.filtroGenero);
    },
    
    getCompatibilityClass(percentage) {
      if (percentage >= 80) return 'excellent';
      if (percentage >= 60) return 'good';
      if (percentage >= 40) return 'average';
      return 'low';
    },
    
    formatFecha(fechaISO) {
      const fecha = new Date(fechaISO);
      return fecha.toLocaleDateString() + ' ' + fecha.toLocaleTimeString();
    },
    
    formatGenero(genero) {
      const generos = {
        'masculino': 'Masculino',
        'femenino': 'Femenino',
        'no_binario': 'No binario',
        'prefiero_no_decir': 'Prefiero no decir'
      };
      return generos[genero] || 'No especificado';
    }
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow-x: hidden;
}

.bg-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.floating-heart {
  position: absolute;
  font-size: 2rem;
  opacity: 0.1;
  animation: float 6s ease-in-out infinite;
}

.heart-1 {
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.heart-2 {
  top: 20%;
  right: 15%;
  animation-delay: 2s;
}

.heart-3 {
  bottom: 30%;
  left: 20%;
  animation-delay: 4s;
}

.heart-4 {
  bottom: 10%;
  right: 10%;
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}

.dashboard > * {
  position: relative;
  z-index: 1;
}

.header {
  padding: 2rem;
  margin-bottom: 2rem;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.title-section {
  text-align: left;
}

.main-title {
  font-size: 2.8rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #ff6b6b, #ee5a24, #ff9ff3, #54a0ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.heart-icon {
  font-size: 3rem;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.subtitle {
  font-size: 1.2rem;
  color: #6c757d;
  margin: 0.5rem 0 0 0;
  font-weight: 300;
}

.logout-btn {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(238, 90, 36, 0.3);
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(238, 90, 36, 0.4);
}

.filters {
  max-width: 1200px;
  margin: 0 auto 3rem auto;
  padding: 0 2rem;
}

.filters > div {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.filter-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 1.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-icon {
  font-size: 1.3rem;
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-option {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 1rem 1.5rem;
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.7);
  border: 2px solid transparent;
  transition: all 0.3s ease;
  font-weight: 500;
}

.filter-option:hover {
  background: rgba(84, 160, 255, 0.1);
  border-color: rgba(84, 160, 255, 0.3);
  transform: translateY(-2px);
}

.filter-option.active {
  background: linear-gradient(135deg, #54a0ff, #2e86de);
  color: white;
  border-color: #54a0ff;
  box-shadow: 0 4px 15px rgba(84, 160, 255, 0.3);
}

.filter-option input[type="radio"] {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.radio-custom {
  width: 20px;
  height: 20px;
  border: 2px solid #ddd;
  border-radius: 50%;
  position: relative;
  transition: all 0.3s ease;
}

.filter-option.active .radio-custom {
  border-color: white;
  background: white;
}

.filter-option.active .radio-custom::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: #54a0ff;
  border-radius: 50%;
}

.matches-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem 2rem 2rem;
}

.section-header h3 {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.matches-icon {
  font-size: 2.2rem;
}

.count {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(84, 160, 255, 0.3);
  border-left: 4px solid #54a0ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading p {
  font-size: 1.2rem;
  color: #6c757d;
  font-weight: 500;
}

.no-matches {
  text-align: center;
  padding: 4rem 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.no-matches-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.no-matches h4 {
  font-size: 1.5rem;
  color: #333;
  margin: 0 0 1rem 0;
  font-weight: 600;
}

.no-matches p {
  color: #6c757d;
  font-size: 1.1rem;
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.match-card {
  position: relative;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.4s ease;
  animation: slideUp 0.6s ease forwards;
  opacity: 0;
  transform: translateY(30px);
  overflow: hidden;
}

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.match-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
}

.match-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(135deg, #ff6b6b, #54a0ff, #5f27cd, #ff9ff3);
  border-radius: 26px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.match-card:hover .match-glow {
  opacity: 0.7;
}

.match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(0, 0, 0, 0.05);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6b6b, #54a0ff);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.match-header h4 {
  margin: 0;
  color: #333;
  font-size: 1.4rem;
  font-weight: 600;
}

.compatibility-badge {
  text-align: center;
  padding: 0.75rem 1rem;
  border-radius: 16px;
  color: white;
  font-weight: 700;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  min-width: 80px;
}

.compatibility-badge.excellent {
  background: linear-gradient(135deg, #00d2ff, #3a7bd5);
}

.compatibility-badge.good {
  background: linear-gradient(135deg, #11998e, #38ef7d);
}

.compatibility-badge.average {
  background: linear-gradient(135deg, #ffa726, #ff7043);
}

.compatibility-badge.low {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
}

.percentage {
  font-size: 1.2rem;
  line-height: 1;
}

.compatibility-text {
  font-size: 0.8rem;
  opacity: 0.9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.match-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: rgba(0, 0, 0, 0.02);
  border-radius: 12px;
  transition: background 0.3s ease;
}

.info-item:hover {
  background: rgba(84, 160, 255, 0.05);
}

.label {
  font-weight: 600;
  color: #495057;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-icon {
  font-size: 1.1rem;
}

.value {
  color: #6c757d;
  font-weight: 500;
}

.match-actions {
  display: flex;
  gap: 1rem;
}

.action-btn {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.action-btn.primary {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  color: white;
  box-shadow: 0 4px 15px rgba(238, 90, 36, 0.3);
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(238, 90, 36, 0.4);
}

.action-btn.secondary {
  background: rgba(84, 160, 255, 0.1);
  color: #54a0ff;
  border: 1px solid rgba(84, 160, 255, 0.3);
}

.action-btn.secondary:hover {
  background: rgba(84, 160, 255, 0.2);
  transform: translateY(-2px);
}

.error {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 1.5rem 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  color: #dc3545;
  border-left: 4px solid #dc3545;
  display: flex;
  align-items: center;
  gap: 1rem;
  font-weight: 500;
  box-shadow: 0 4px 15px rgba(220, 53, 69, 0.2);
}

.error-icon {
  font-size: 1.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
    padding: 1.5rem;
  }
  
  .main-title {
    font-size: 2.2rem;
  }
  
  .filter-options {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-option {
    justify-content: center;
  }
  
  .matches-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .match-actions {
    flex-direction: column;
  }
  
  .dashboard {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .main-title {
    font-size: 1.8rem;
  }
  
  .match-card {
    padding: 1.5rem;
  }
  
  .header, .matches-section, .filters {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>