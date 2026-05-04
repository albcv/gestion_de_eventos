import axios from './axios';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email?: string;
  password: string;
  [key: string]: any;
}

export interface LoginResponse {
  user?: any;
}

export const fetchCsrfCookie = async (): Promise<void> => {
  await axios.get('/csrf/');
};

export const loginUser = async (username: string, password: string): Promise<LoginResponse> => {
  try {
    const response = await axios.post('/login/', { username, password });
  
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw new Error(error.response.data.Error || 'Error en el login');
    } else if (error.request) {
      throw new Error('No se pudo conectar al servidor');
    } else {
      throw new Error('Error al enviar la petición');
    }
  }
};

export const registerUser = async (userData: RegisterData): Promise<any> => {
  try {
    const response = await axios.post('/register/', userData);
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw error.response.data;
    } else if (error.request) {
      throw new Error('No se pudo conectar al servidor');
    } else {
      throw new Error('Error al enviar la petición');
    }
  }
};

export const logoutUser = async (): Promise<void> => {
  try {
    await axios.post('/logout/');
   
  } catch (error) {
    console.error('Error al cerrar sesión', error);
  }
};