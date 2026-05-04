// src/services/evento.ts
import axios from './axios'; 

export interface EventoActual {
  id: number;
  nombre: string;
  fecha_apertura: string;
  fecha_cierre: string;
  entidad_patrocinadora: string;
  tematicas: string[];
  rol_usuario: 'participante' | 'oponente' | null;
}

export const getEventoActual = async (): Promise<EventoActual> => {
  try {
    const response = await axios.get<EventoActual>('/evento-actual/');
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Error al obtener el evento');
    } else if (error.request) {
      throw new Error('No se pudo conectar al servidor');
    } else {
      throw new Error('Error al enviar la petición');
    }
  }
};