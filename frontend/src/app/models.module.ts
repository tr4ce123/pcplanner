export interface Preferences {
  id: number,
  budget: number
}

export interface AIResponse {
  response: string
}

export interface Component {
  name: string;
  price: number;
}

export interface Computer {
  id: number;
  components: {
    cpu: Component;
    cpuCooler: Component;
    gpu: Component;
    motherboard: Component;
    ram: Component;
    psu: Component;
    storage: Component;
    case: Component;
  }
  totalPrice: number;
}