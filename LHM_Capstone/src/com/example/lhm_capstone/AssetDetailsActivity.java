package com.example.lhm_capstone;

import android.R.string;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.ActionBar;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.os.Build;

public class AssetDetailsActivity extends ActionBarActivity {
	Button buttonSubmit;
	Spinner spinnerStatus, spinnerOk, spinnerAction;
	TextView assetMakeName, assetModelName, assetVINID;
	CharSequence modelName, makeName, VinId;
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_asset_details);

        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new PlaceholderFragment())
                    .commit();
        }
        assetMakeName = (TextView)findViewById(R.id.assetMakeName);
        assetMakeName.append(makeName);
        assetModelName = (TextView)findViewById(R.id.assetModelName);
        assetModelName.append(modelName);
        assetVINID = (TextView)findViewById(R.id.assetVINID);
        assetVINID.append(VinId);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.asset_details, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    /**
     * A placeholder fragment containing a simple view.
     */
    public static class PlaceholderFragment extends Fragment {

        public PlaceholderFragment() {
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState) {
            View rootView = inflater.inflate(R.layout.fragment_asset_details, container, false);
            return rootView;
        }
    }
    
    public void sendMessage(View view)
    {
    	//update database with spinner selections and link to next activity
    	//not really sure how to do it, but leaving this here for now
    }

}
