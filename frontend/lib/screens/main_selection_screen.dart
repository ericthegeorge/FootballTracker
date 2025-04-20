import 'package:flutter/material.dart';
import 'package:frontend/routes.dart';

class MainSelectionScreen extends StatelessWidget {
  // Navigation to different screens
  void navigateToScreen(BuildContext context, String screen) {
    switch (screen) {
      case 'league':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => LeagueScreen()),
        );
        break;
      case 'team':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => TeamScreen()),
        );
        break;
      case 'player':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => PlayerScreen()),
        );
        break;
      case 'matches':
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => MatchesScreen()),
        );
        break;
      default:
        print('Invalid screen');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Main Selection Screen')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () => navigateToScreen(context, Routes.leagues),
              child: Text('Leagues'),
            ),
            ElevatedButton(
              onPressed: () => navigateToScreen(context, Routes.teams),
              child: Text('Teams'),
            ),
            ElevatedButton(
              onPressed: () => navigateToScreen(context, Routes.players),
              child: Text('Players'),
            ),
            ElevatedButton(
              onPressed: () => navigateToScreen(context, Routes.matches),
              child: Text('Matches'),
            ),
            ElevatedButton(
              onPressed:
                  () => navigateToScreen(context, Routes.account_settings),
              child: Text('Account Settings'),
            ),
          ],
        ),
      ),
    );
  }
}

// Dummy screens for each option
class LeagueScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('League Screen')),
      body: Center(child: Text('This is the League screen')),
    );
  }
}

class TeamScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Team Screen')),
      body: Center(child: Text('This is the Team screen')),
    );
  }
}

class PlayerScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Player Screen')),
      body: Center(child: Text('This is the Player screen')),
    );
  }
}

class MatchesScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Matches Screen')),
      body: Center(child: Text('This is the Matches screen')),
    );
  }
}

class AccountSettingsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Account Settings Screen')),
      body: Center(child: Text('This is the Account Settings screen')),
    );
  }
}
