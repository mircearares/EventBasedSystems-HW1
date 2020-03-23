# EventBasedSystems-HW1

Input: 2 json files
  * one containing the domain I have chosen
  * and the other one containing some weights for fields
  
Group the fields based on the domains, using the *create_gorups* function, will generate an list of groups, each group containing several fields, trying to group in a balanced way the fields.

Then we process the newly created groups with *compute_frequency_per_field* by calculating the possible frequency based on the configured number of messages.

We then pass these groups with the domain to the *generate_subscriptions* function, which will return a dictionary containing subscriptions.

Then, function *generate_publications* will create several publications.

These two generated dictionaries will be written in separate files
