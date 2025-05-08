export type Products = {
    id:string;
    name:string;
    description:string;
    cost:number;
  };
  
  export type AgentState = {
    model: string;
    logs: any[];
    products: Products[]
  }