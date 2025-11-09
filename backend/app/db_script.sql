-- Password : test@123
INSERT INTO public.users(
	email, hashed_password, is_active, is_superuser, first_name, last_name, role, created_at, updated_at)
	VALUES ('admin_it@exemple.com', '$2b$12$JO5poKR0yuaoqTyiPcyCiuJ6AQDq9hvWbRzO.pVlL1JsGKcldP2mW', True, 
	False, 'Sam', 'Walton' , 'admin', Now(), Now())


INSERT INTO public.departments(
	name, code, description, is_active, created_at, updated_at)
	VALUES ('IT', 'IT', 'IT Department', True, Now(), Now());


INSERT INTO public.department_admins(department_id, user_id, is_active, created_at, updated_at)
	                                VALUES (1, 3, True, Now(), Now());