import React from "react";

const UserRegistrationForm = ({ newUser, setNewUser, onSubmit, error }) => {
  return (
    <>
        <p>{error && <p className="error">{error}</p>}</p>
        <section className="row">
            <div className="row-items">

            </div>
        </section>

        <section className="row">
            <div className="row-items">
                <label htmlFor="first_name">First Name</label>
                <input
                    type="text"
                    name="first_name"
                    placeholder="First Name"
                    value={newUser.first_name}
                    onChange={(e) =>
                    setNewUser({ ...newUser, first_name: e.target.value })
                    }
                />
            </div>
            
            <div className="row-items">
                <label htmlFor="middle_name">Middle Name</label>
                <input
                    type="text"
                    name="middle_name"
                    placeholder="Middle Name (Optional)"
                    value={newUser.middle_name}
                    onChange={(e) =>
                    setNewUser({ ...newUser, middle_name: e.target.value })
                    }
                />
            </div>

            <div className="row-items">
                <label htmlFor="last_name">Last Name</label>
                <input
                    type="text"
                    name="last_name"
                    placeholder="Last Name"
                    value={newUser.last_name}
                    onChange={(e) =>
                    setNewUser({ ...newUser, last_name: e.target.value })
                    }
                />
            </div>
        </section>
        
        <section className="row">
            <div className="row-items">
                <label htmlFor="school_name">School Name</label>
                <input
                    type="text"
                    name="school_name"
                    placeholder="School Name"
                    value={newUser.school_name}
                    onChange={(e) =>
                    setNewUser({ ...newUser, school_name: e.target.value })
                    }
                />
            </div>

            <div className="row-items">
                <label htmlFor="email">Email</label>
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={newUser.email}
                    onChange={(e) =>
                    setNewUser({ ...newUser, email: e.target.value })
                    }
                />
            </div>

            <div className="row-items">
                <label htmlFor="role">Role</label>
                <select
                    name="role"
                    value={newUser.role}
                    onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                >
                    <option value="student">Student</option>
                    <option value="teacher">Teacher</option>
                    <option value="admin">Admin</option>
                </select>
            </div>
        </section>

        <section className='row'>
            <div className='row-items'  style={{ width: "49%" }}>
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  name="username"
                  placeholder="Username"
                  value={newUser.username}
                  onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                />
            
            </div>
            <div className='row-items'  style={{ width: "49%" }}>
              <label htmlFor="password">Password</label>
                <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  value={newUser.password}
                  onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                />
            </div>
        </section>

    </>
  );
};

export default UserRegistrationForm;
