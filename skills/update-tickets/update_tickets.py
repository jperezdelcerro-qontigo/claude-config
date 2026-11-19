import argparse
import re
from dbtools.bin.release_utils import construct_jira_ticket_url, jira_authenticate

from datetime import datetime
import pytz

def add_comment(jira, issue_key, user_name, environment):
    now = datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M %Z')
    comment = f"Ticket status updated by {user_name}. Deployed on {now} to {environment}"
    try:
        jira.add_comment(issue_key, comment)
        print(f"📝 Added comment to {construct_jira_ticket_url(issue_key)}")
    except Exception as e:
        print(f"⚠️ Failed to add comment to {construct_jira_ticket_url(issue_key)}: {e}")


def update_environment(jira, issue_key, environment_value, env_field_id="customfield_10056"):
    try:
        issue = jira.issue(issue_key)
        current_env = getattr(issue.fields, env_field_id, None)

        # Manejo seguro del objeto CustomFieldOption
        current_value = getattr(current_env, "value", None)

        if current_value != environment_value:
            issue.update(fields={env_field_id: {"value": environment_value}})
            print(f"🌱 Updated Environment to '{environment_value}' for {construct_jira_ticket_url(issue_key)}")
        else:
            print(f"ℹ️ Environment already set to '{environment_value}' for {construct_jira_ticket_url(issue_key)}")

    except AttributeError as ae:
        print(f"⚠️ Attribute error while updating Environment for {construct_jira_ticket_url(issue_key)}: {ae}")
    except Exception as e:
        print(f"❌ Error updating Environment for {construct_jira_ticket_url(issue_key)}: {e}")



def transition_to_status(jira, issue_key, target_status):
    transitions = jira.transitions(issue_key)
    transition_id = None
    for t in transitions:
        if t["name"].lower() == target_status.lower():
            transition_id = t["id"]
            break
    if transition_id:
        jira.transition_issue(issue_key, transition_id)
        print(f"✅ Transitioned {construct_jira_ticket_url(issue_key)} to '{target_status}'")
    else:
        print(f"⚠️ No transition found to '{target_status}' for {construct_jira_ticket_url(issue_key)}")

def parse_ticket_string(ticket_string):
    return [ticket.strip() for ticket in re.split(r'[,\s]+', ticket_string.strip()) if ticket.strip()]


def update_fix_version_and_gallery(jira, issue_key, version_name, gallery_value="UI Gallery Master", gallery_field_id="customfield_12345"):
    issue = jira.issue(issue_key)
    fix_versions = issue.fields.fixVersions

    try:
        project_key = issue_key.split("-")[0]
        versions = jira.project_versions(project_key)
        matching_version = next((v for v in versions if v.name == version_name), None)

        update_fields = {
            gallery_field_id: {"value": gallery_value}
        }

        if not fix_versions and matching_version:
            update_fields["fixVersions"] = [{"id": matching_version.id}]
            print(f"🔧 Set Fix Version '{version_name}' and Gallery '{gallery_value}' for {construct_jira_ticket_url(issue_key)}")
        else:
            print(f"ℹ️ {construct_jira_ticket_url(issue_key)} already has Fix Version(s), updated Gallery to '{gallery_value}'")

        issue.update(fields=update_fields)

    except Exception as e:
        print(f"❌ Error updating Fix Version or Gallery for {construct_jira_ticket_url(issue_key)}: {e}")



def main():
    parser = argparse.ArgumentParser(description="Update JIRA tickets with a label and transition to a new status.")
    parser.add_argument("--tickets", required=True, help="List of JIRA ticket numbers (e.g., MAC-1234 XYZ-5678)")
    parser.add_argument("--env", required=True, help="Environment label to add (e.g., staging, production)")
    parser.add_argument("--user", required=False, default="jperez")
    parser.add_argument("--fix-version", required=False, help="Fix version to set if none exists (e.g., 1.2.3)")
    parser.add_argument("--update-gallery", required=False, default=False)
    args = parser.parse_args()
    tickets = parse_ticket_string(args.tickets)
    for ticket in tickets:
        try:
            
            jira = jira_authenticate()
            if not jira:
                print("❌ Failed to authenticate to JIRA.")
                return
            
            if args.update_gallery:
                update_fix_version_and_gallery(jira, ticket, "UI Gallery Master")
            else: 
                update_environment(jira, ticket, args.env)
                transition_to_status(jira, ticket, "Needs testing")
                add_comment(jira, ticket, args.user, args.env)
        except Exception as e:
            print(f"❌ Error processing {construct_jira_ticket_url(ticket)}: {e}")

if __name__ == "__main__":
    main()

