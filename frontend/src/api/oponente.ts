import axios from './axios';

export interface Version {
  id: number;
  version_numero: number;
  nombre_archivo: string;
  tipo_archivo: string;
  tamanio: number;
  descripcion: string;
  fecha_subida: string;
}

export interface TrabajoTribunal {
  id: number;
  titulo: string;
  participante: string;
  tematica: string;
  evento: string;
  aprobado: boolean;
  powerpoint?: { url: string; nombre_archivo: string } | null;
  versiones: Version[];
}

export const obtenerTrabajosTribunal = async (): Promise<TrabajoTribunal[]> => {
  const response = await axios.get('/trabajos-tribunal/');
  return response.data;
};

export const descargarVersionTribunal = async (versionId: number): Promise<Blob> => {
  const response = await axios.get(`/descargar-version/${versionId}/`, {
    responseType: 'blob',
  });
  return response.data;
};

export const aprobarTrabajo = async (trabajoId: number): Promise<{ message: string }> => {
  const response = await axios.post(`/aprobar-trabajo/${trabajoId}/`);
  return response.data;
};

export const agregarNoConformidad = async (versionId: number, texto: string): Promise<any> => {
  const response = await axios.post('/agregar-no-conformidad/', { version_id: versionId, texto });
  return response.data;
};

export const obtenerNoConformidades = async (versionId: number): Promise<any[]> => {
  const response = await axios.get(`/no-conformidades/${versionId}/`);
  return response.data;
};

export const editarNoConformidad = async (ncId: number, texto: string): Promise<any> => {
  const response = await axios.put(`/editar-no-conformidad/${ncId}/`, { texto });
  return response.data;
};

export const eliminarNoConformidad = async (ncId: number): Promise<void> => {
  await axios.delete(`/eliminar-no-conformidad/${ncId}/`);
};

export const descargarPowerpointTribunal = async (trabajoId: number): Promise<Blob> => {
  const response = await axios.get(`/descargar-powerpoint-tribunal/${trabajoId}/`, {
    responseType: 'blob',
  });
  return response.data;
};