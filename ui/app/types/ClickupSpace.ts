export interface ClickupSpace {
  spaces: Space[];
}

export interface Space {
  admin_can_manage: boolean | null;
  archived: boolean;
  avatar: null;
  color: string;
  features: Features;
  id: string;
  members: Member[];
  multiple_assignees: boolean;
  name: string;
  private: boolean;
  statuses: Status[];
}

export interface Features {
  check_unresolved: CheckUnresolved;
  custom_fields: CustomFields;
  custom_items: CustomItems;
  dependency_warning?: DependencyWarning;
  due_dates: DueDates;
  emails: Emails;
  milestones: Milestones;
  multiple_assignees?: MultipleAssignees;
  points: Points;
  priorities: Priorities;
  remap_dependencies: RemapDependencies;
  scheduler_enabled: boolean;
  sprints: Sprints;
  status_pies: StatusPies;
  tags: Tags;
  time_estimates: TimeEstimates;
  time_tracking: TimeTracking;
}

export interface CheckUnresolved {
  checklists: null;
  comments: null;
  enabled: boolean;
  subtasks: null | boolean;
}

export interface CustomFields {
  enabled: boolean;
}

export interface CustomItems {
  enabled: boolean;
}

export interface DependencyWarning {
  enabled: boolean;
}

export interface DueDates {
  enabled: boolean;
  remap_closed_due_date: boolean;
  remap_due_dates: boolean;
  start_date: boolean;
}

export interface Emails {
  enabled: boolean;
}

export interface Milestones {
  enabled: boolean;
}

export interface MultipleAssignees {
  enabled: boolean;
}

export interface Points {
  enabled: boolean;
}

export interface Priorities {
  enabled: boolean;
  priorities: Priority[];
}

export interface Priority {
  color: string;
  id: string;
  orderindex: string;
  priority: string;
}

export interface RemapDependencies {
  enabled: boolean;
}

export interface Sprints {
  enabled: boolean;
}

export interface StatusPies {
  enabled: boolean;
}

export interface Tags {
  enabled: boolean;
}

export interface TimeEstimates {
  enabled: boolean;
  per_assignee: boolean;
  rollup: boolean;
}

export interface TimeTracking {
  default_to_billable: number;
  enabled: boolean;
  harvest: boolean;
  rollup: boolean;
}

export interface Member {
  user: User;
}

export interface User {
  color: string;
  id: number;
  initials: string;
  profilePicture: null;
  username: string;
}

export interface Status {
  color: string;
  id: string;
  orderindex: number;
  status: string;
  type: string;
}
