import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import axios from "axios";
const schema = z
  .object({
    email: z.string().min(5, { message: "Email must be at least 5 characters long" }),
    username: z.string().min(1, {message: "Username is required"}),
    first_name: z.string().min(1, {message: "First name is required"}),
    last_name: z.string().min(1, {message: "Last name is required"}).max(100, {message: "Last name must be at most 100 characters long"}),
    password: z.string().min(6, {message: "Password must be at least 6 characters long"}).max(18, {message: "Password must be at most 18 characters long"}),
    role: z.string().min(1, { message: "Role is required" }),
  })
  .strict();

type CreateUserRequest = z.infer<typeof schema>;

const Form = () => {
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CreateUserRequest>({
    resolver: zodResolver(schema),
  });

    const onSubmit = (data: CreateUserRequest) => {
        console.log("Form submitted with data:", data);
        axios
        .post(`http://localhost:8000/auth`, data)
        .then((response) => {
            console.log("User created successfully:", response.data);
        })
        .catch((error) => {
            console.error("Error creating user:", error);
        });
    };


  return (
    <form
      className="form-container"
      onSubmit={handleSubmit(onSubmit)}
    >
      <h2>Create User</h2>
      <div className="mb-3">
        <input
          className="form-control"
          {...register("email")}
          placeholder="Email"
        />
        {errors.email && <p className="text-danger">{errors.email.message}</p>}
      </div>

      <div className="mb-3">
        <input
          className="form-control"
          {...register("username")}
          placeholder="Username"
        />
        {errors.username && <p className="text-danger">{errors.username.message}</p>}
      </div>

      <div className="mb-3">
        <input
          className="form-control"
          {...register("first_name")}
          placeholder="First Name"
        />
        {errors.first_name && <p className="text-danger">{errors.first_name.message}</p>}
      </div>
      <div className="mb-3">
        <input
          className="form-control"
          {...register("last_name")}
          placeholder="Last Name"
        />
        {errors.last_name && <p className="text-danger">{errors.last_name.message}</p>}
      </div>
          <div className="mb-3">
        <select className="form-select" {...register("role")}>
          <option value="">Select a role</option>
          <option value="admin">Admin</option>
          <option value="user">User</option>
        </select>
        {errors.role && <p className="text-danger">{errors.role.message}</p>}
      </div>
      <div className="mb-3">
        <input
            {...register("password")}
          className="form-control"
          type={showPassword ? "text" : "password"}
          placeholder="Password"
        />
        {errors.password && <p className="text-danger">{errors.password.message}</p>}
      </div>



      <div className="mb-3 form-check">
        <input
            className="form-check-input"
          type="checkbox"
          checked={showPassword}
          onChange={() => setShowPassword(!showPassword)}
        />
        <label className="form-check-label">Show Password</label>
      </div>
      <button className="btn btn-outline-primary" type="submit">Submit</button>
    </form>
  );
};

export default Form;
