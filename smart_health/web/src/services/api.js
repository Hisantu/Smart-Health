import axios from "axios"
import { io } from "socket.io-client"

export const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:4000/api"
})

export const socket = io(import.meta.env.VITE_API_URL?.replace('/api', '') || "http://localhost:4000")
