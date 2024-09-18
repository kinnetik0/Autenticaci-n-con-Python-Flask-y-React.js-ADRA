import React, { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

import { Context } from "../store/appContext";

export const Login = () => {
	const { store, actions } = useContext(Context);
	const navigate=useNavigate()

	async function submitForm(e){
		let formData=new FormData(e.target)
		let email=formData.get("email")
		let password=formData.get("password")
		console.log({email, password})
		let logged=await actions.login(email, password)
		if (logged) navigate("/")
	}

	return (
		<div className="container">
			<form onSubmit={submitForm}>
  <div class="mb-3">
    <label htmlFor="exampleInputEmail1" class="form-label">Email address</label>
    <input name="email" type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" />
    <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
  </div>
  <div class="mb-3">
    <label htmlFor="exampleInputPassword1" class="form-label">Password</label>
    <input name="password" type="password" class="form-control" id="exampleInputPassword1" />
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
			
		</div>
	);
};
