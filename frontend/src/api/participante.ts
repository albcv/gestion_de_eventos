import axios from './axios';

export interface CrearTrabajoResponse {
  mensaje: string;
  trabajo_id: number;
  version: number;
  archivo: string;
}

export interface Version {
  id: number;
  version_numero: number;
  nombre_archivo: string;
  tipo_archivo: string;
  tamanio: number;
  descripcion: string;
  fecha_subida: string;
  archivo_url: string;
  no_conformidades?: { id: number; no_conformidad: string }[];
}

export interface MiTrabajoResponse {
  trabajo_existe: boolean;
  trabajo?: {
    id: number;
    titulo: string;
    tematica: string;
    aprobado?: boolean;
    powerpoint?: {
      url: string;
      nombre_archivo: string;
    } | null;
    versiones: Version[];
  };
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

  const response = await axios.post<CrearTrabajoResponse>('/trabajos/crear/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const obtenerMiTrabajo = async (): Promise<MiTrabajoResponse> => {
  const response = await axios.get('/mi-trabajo/');
  return response.data;
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
  
  const response = await axios.post('/crear-version/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const descargarVersion = async (versionId: number): Promise<Blob> => {
  const response = await axios.get(`/descargar-version/${versionId}/`, {
    responseType: 'blob',
  });
  return response.data;
};

export const subirPowerpoint = async (archivo: File): Promise<{ message: string; url: string }> => {
  const formData = new FormData();
  formData.append('archivo', archivo);
  const response = await axios.post('/subir-powerpoint/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const descargarPowerpoint = async (): Promise<Blob> => {
  const response = await axios.get('/descargar-powerpoint/', {
    responseType: 'blob',
  });
  return response.data;
};