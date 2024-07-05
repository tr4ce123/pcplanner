export interface Preferences {
  id: number,
  budget: number,
  chipset: string,
  need_wifi: boolean
  usage: string
}

export interface AIResponse {
  response: string
}

export interface computerComponent {
  type: string | null;
  name: string;
  price: number;
  pcpp_url: string | null;
  specs: any | null;
  image_url: string | null;
  rating: number | null;
}

export interface Computer {
  id: number;
  name: string;
  components: {
    cpu: computerComponent;
    cpuCooler: computerComponent;
    gpu: computerComponent;
    motherboard: computerComponent;
    ram: computerComponent;
    psu: computerComponent;
    storage: computerComponent;
    case: computerComponent;
  }
  total_price: number;
}