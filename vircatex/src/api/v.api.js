import axios from 'axios'

export const getAllData = () => {
    return axios.get('http://127.0.0.1:8000/sistema/acabado/')
}