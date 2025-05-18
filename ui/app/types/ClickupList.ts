export interface ClickupList {
  lists: List[];
}

export interface List {
  id: string;
  name: string;
  orderindex: number;
  status?: {
    color: string;
    status: string;
    type: string;
  } | null;
  priority?: {
    color: string;
    id: string;
    orderindex: string;
    priority: string;
  } | null;
  assignee?: null;
  task_count?: number;
  due_date?: string | null;
  start_date?: string | null;
  folder?: {
    id: string;
    name: string;
    hidden: boolean;
    access: boolean;
  } | null;
  space?: {
    id: string;
    name: string;
  };
  space_id?: string; // Added for our UI
  archived: boolean;
  override_statuses?: boolean;
  permission_level?: string;
}
