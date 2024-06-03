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
  pcpp_url: string | null;
  specs: any | null;
  image_url: string | null;
}

export interface Computer {
  id: number;
  name: string;
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
  total_price: number;
}