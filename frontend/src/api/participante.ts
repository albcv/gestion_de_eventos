import axios from './axios';

export interface CrearTrabajoResponse {
  mensaje: string;
  trabajo_id: number;
  version: number;
  archivo: string;
}

export const crearTrabajo = async (
  titulo: string,
  tematica_id: number,
  archivo: File,
  descripcion?: string
): Promise<CrearTrabajoResponse> => {
  const formData = new FormData();
  formData.append('titulo', titulo);
  formData.append('tematica_id', tematica_id.toString());
  formData.append('archivo', archivo);
  if (descripcion) formData.append('descripcion', descripcion);

  try {
    const response = await axios.post<CrearTrabajoResponse>('/trabajos/crear/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Error al crear el trabajo');
    } else if (error.request) {
      throw new Error('No se pudo conectar al servidor');
    } else {
      throw new Error('Error al enviar la petición');
    }
  }
};

export interface Version {
  id: number;
  version_numero: number;
  nombre_archivo: string;
  tipo_archivo: string;
  tamanio: number;
  descripcion: string;
  fecha_subida: string;
  archivo_url: string;
  no_conformidades?: { id: number; no_conformidad: string }[]; // Nuevo
}

export interface MiTrabajoResponse {
  trabajo_existe: boolean;
  trabajo?: {
    id: number;
    titulo: string;
    tematica: string;
    aprobado?: boolean;      
    versiones: Version[];
  };
}

export const obtenerMiTrabajo = async (): Promise<MiTrabajoResponse> => {
  try {
    const response = await axios.get('/mi-trabajo/');
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Error al obtener trabajo');
    }
    throw new Error('Error de conexión');
  }
};

export const crearVersion = async (
  trabajo_id: number,
  archivo: File,
  descripcion?: string
): Promise<{ mensaje: string; version: number; archivo_url: string }> => {
  const formData = new FormData();
  formData.append('trabajo_id', trabajo_id.toString());
  formData.append('archivo', archivo);
  if (descripcion) formData.append('descripcion', descripcion);
  
  try {
    const response = await axios.post('/crear-version/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.error || 'Error al crear versión');
    }
    throw new Error('Error de conexión');
  }
};


export const descargarVersion = async (versionId: number): Promise<Blob> => {
  try {
    const response = await axios.get(`/descargar-version/${versionId}/`, {
      responseType: 'blob', 
    });
    return response.data;
  } catch (error: any) {
    if (error.response) {
      // Intenta extraer el mensaje de error del blob (puede ser JSON)
      const text = await error.response.data.text();
      try {
        const json = JSON.parse(text);
        throw new Error(json.error || 'Error al descargar versión');
      } catch {
        throw new Error('Error al descargar versión');
      }
    }
    throw new Error('Error de conexión');
  }
};