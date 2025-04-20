import 'package:flutter/material.dart';
// import 'package:frontend/screens/main_selection_screen.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/main_selection_screen.dart';

class Routes {
  static const String home = '/home';
  static const String login = '/login';
  static const String register = '/register';
  static const String main_selection = '/main_selection';
  static const String leagues = '/leagues';
  static const String teams = '/teams';
  static const String players = '/players';
  static const String matches = '/matches';
  static const String account_settings = '/account_settings';

  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case home:
        return MaterialPageRoute(builder: (_) => HomeScreen());
      case login:
        return MaterialPageRoute(builder: (_) => LoginScreen());
      case register:
        return MaterialPageRoute(builder: (_) => RegisterScreen());
      case main_selection:
        return MaterialPageRoute(builder: (_) => MainSelectionScreen());
      default:
        return MaterialPageRoute(
          builder: (_) => HomeScreen(),
        ); // or an error screen
    }
  }
}
