export interface ClickupTask {
  tasks: Task[];
}

export interface Task {
  id: string;
  name: string;
  custom_id?: string;
  text_content?: string;
  description?: string;
  status?: {
    status: string;
    color: string;
    type: string;
    orderindex: number;
  } | null;
  orderindex?: string;
  date_created?: string;
  date_updated?: string;
  date_closed?: string;
  creator?: {
    id: number;
    username: string;
    email: string;
    color: string;
    profilePicture: string;
  };
  assignees?: {
    id: number;
    username: string;
    email: string;
    color: string;
    profilePicture: string;
  }[];
  priority?: {
    id: string;
    priority: string;
    color: string;
    orderindex: string;
  } | null;
  due_date?: string | null;
  start_date?: string | null;
  time_estimate?: number | null;
  list?: {
    id: string;
    name: string;
  };
  list_id?: string; // Added for our UI
  folder?: {
    id: string;
    name: string;
  };
  space?: {
    id: string;
    name: string;
  };
  tags?: {
    name: string;
    tag_fg: string;
    tag_bg: string;
  }[];
}
