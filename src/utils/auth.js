// Mock authentication functions
let currentUser = null;

// Check if user is authenticated
export const checkAuth = () => {
  const userData = localStorage.getItem('currentUser');
  if (userData) {
    currentUser = JSON.parse(userData);
    return currentUser;
  }
  return null;
};

// Login function
export const login = async (email, password) => {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Mock validation - in real app, this would be an API call
  if (email === 'demo@example.com' && password === 'password') {
    const user = {
      id: 1,
      email: email,
      firstName: 'John',
      lastName: 'Doe'
    };
    localStorage.setItem('currentUser', JSON.stringify(user));
    currentUser = user;
    return user;
  }
  
  throw new Error('Invalid email or password');
};

// Register function
export const register = async (email, password, firstName, lastName) => {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Mock registration - in real app, this would be an API call
  const user = {
    id: Date.now(),
    email,
    firstName,
    lastName
  };
  
  localStorage.setItem('currentUser', JSON.stringify(user));
  currentUser = user;
  return user;
};

// Logout function
export const logout = () => {
  localStorage.removeItem('currentUser');
  currentUser = null;
};

// Get current user
export const getCurrentUser = () => {
  return currentUser;
};
