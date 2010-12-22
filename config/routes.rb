Jamiecurle::Application.routes.draw do
  #
  #
  #
  
  controller :sessions do
    get 'login' => :new
    post 'login' => :create
    delete 'logout' => :destroy
  end
  
  #
  #
  #
  resources :users
  resources :posts
  #
  # This is the root
  #
  root :to => "posts#index"
end