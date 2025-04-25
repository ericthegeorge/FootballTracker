import 'package:flutter/material.dart';
// import 'package:frontend/screens/main_selection_screen.dart';
import 'screens/home_screen.dart';

import 'screens/login_screen.dart';
import 'screens/register_screen.dart';

import 'screens/main_selection_screen.dart';

import 'screens/leagues/leagues_screen.dart';
import 'screens/teams/teams_screen.dart';
import 'screens/players/players_screen.dart';
import 'screens/matches/matches_screen.dart';
import 'screens/account_settings_screen.dart';

// Leagues screens
import 'screens/leagues/leagues_view_screen.dart';
import 'screens/leagues/leagues_search_screen.dart';
import 'screens/leagues/leagues_select_screen.dart';
import 'screens/leagues/leagues_add_screen.dart';

// Teams screens
import 'screens/teams/teams_view_screen.dart';
import 'screens/teams/teams_search_screen.dart';
import 'screens/teams/teams_select_screen.dart';
import 'screens/teams/teams_add_screen.dart';

// Players screens
import 'screens/players/players_view_screen.dart';
import 'screens/players/players_search_screen.dart';
import 'screens/players/players_select_screen.dart';
import 'screens/players/players_add_screen.dart';

// Matches screens
import 'screens/matches/matches_view_screen.dart';
import 'screens/matches/matches_search_screen.dart';
import 'screens/matches/matches_select_screen.dart';
import 'screens/matches/matches_add_screen.dart';

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

  static const String leaguesView = '/leagues/view';
  static const String leaguesSearch = '/leagues/search';
  static const String leaguesSelect = '/leagues/select';
  static const String leaguesAdd = '/leagues/add';

  static const String teamsView = '/teams/view';
  static const String teamsSearch = '/teams/search';
  static const String teamsSelect = '/teams/select';
  static const String teamsAdd = '/teams/add';

  static const String playersView = '/players/view';
  static const String playersSearch = '/players/search';
  static const String playersSelect = '/players/select';
  static const String playersAdd = '/players/add';

  static const String matchesView = '/matches/view';
  static const String matchesSearch = '/matches/search';
  static const String matchesSelect = '/matches/select';
  static const String matchesAdd = '/matches/add';

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

      case leagues:
        return MaterialPageRoute(builder: (_) => LeaguesScreen());
      case teams:
        final league = settings.arguments as String?;
        return MaterialPageRoute(builder: (_) => TeamsScreen(league: league));
      case players:
        return MaterialPageRoute(builder: (_) => PlayersScreen());
      case matches:
        return MaterialPageRoute(builder: (_) => MatchesScreen());
      case account_settings:
        return MaterialPageRoute(builder: (_) => AccountSettingsScreen());

      case leaguesView:
        return MaterialPageRoute(builder: (_) => LeaguesViewScreen());
      case leaguesSearch:
        return MaterialPageRoute(builder: (_) => LeaguesSearchScreen());
      case leaguesSelect:
        return MaterialPageRoute(builder: (_) => LeaguesSelectScreen());
      case leaguesAdd:
        return MaterialPageRoute(builder: (_) => LeaguesAddScreen());

      case teamsView:
        return MaterialPageRoute(builder: (_) => TeamsViewScreen());
      case teamsSearch:
        return MaterialPageRoute(builder: (_) => TeamsSearchScreen());
      case teamsSelect:
        return MaterialPageRoute(builder: (_) => TeamsSelectScreen());
      case teamsAdd:
        return MaterialPageRoute(builder: (_) => TeamsAddScreen());

      case playersView:
        return MaterialPageRoute(builder: (_) => PlayersViewScreen());
      case playersSearch:
        return MaterialPageRoute(builder: (_) => PlayersSearchScreen());
      case playersSelect:
        return MaterialPageRoute(builder: (_) => PlayersSelectScreen());
      case playersAdd:
        return MaterialPageRoute(builder: (_) => PlayersAddScreen());

      case matchesView:
        return MaterialPageRoute(builder: (_) => MatchesViewScreen());
      case matchesSearch:
        return MaterialPageRoute(builder: (_) => MatchesSearchScreen());
      case matchesSelect:
        return MaterialPageRoute(builder: (_) => MatchesSelectScreen());
      case matchesAdd:
        return MaterialPageRoute(builder: (_) => MatchesAddScreen());

      default:
        return MaterialPageRoute(
          builder: (_) => HomeScreen(),
        ); // or an error screen
    }
  }
}
